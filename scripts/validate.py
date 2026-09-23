#!/usr/bin/env python3
"""Validate every app entry.

Hugo performs no validation of its own, so a malformed contribution would
otherwise render as a blank field rather than failing the build. This script is
the only thing standing between a bad pull request and the published site.

Checks run in two groups:

  1. Schema conformance, via schemas/app.schema.json.
  2. Cross-references and invariants the schema cannot express, such as whether
     a device slug actually exists or whether reports are in date order.

Errors fail the build. Warnings do not.
"""

from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime

from jsonschema import Draft202012Validator, FormatChecker

import lib
from lib import EntryError

GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"

BUILD_RE = re.compile(r"^(\d{4})(\d{2})(\d{2})(\d{2})$")

WORKAROUND_REQUIRED = {"possible-with-steps", "possible-via-workaround"}


class Report:
    def __init__(self) -> None:
        self.errors = 0
        self.warnings = 0

    def error(self, path, message, line=None) -> None:
        self.errors += 1
        self._emit("error", path, message, line)

    def warn(self, path, message, line=None) -> None:
        self.warnings += 1
        self._emit("warning", path, message, line)

    def _emit(self, level, path, message, line) -> None:
        rel = str(path.relative_to(lib.ROOT)) if path else "(repo)"
        if GITHUB:
            where = f" file={rel}" + (f",line={line}" if line else "")
            print(f"::{level}{where}::{message}")
        else:
            mark = "error  " if level == "error" else "warning"
            loc = f":{line}" if line else ""
            print(f"{mark} {rel}{loc}: {message}")


def check_enum_drift(report: Report, schema: dict) -> None:
    """The schema duplicates the enum lists in data/. Assert they agree.

    Duplication is unavoidable — JSON Schema cannot read YAML — so it is turned
    into a checked invariant instead of a silent trap.
    """
    reference = lib.load_reference()
    props = schema["properties"]

    expected = {
        "service_type": sorted(reference.service_types),
        "result": sorted(row["value"] for row in reference.statuses["result"]),
        "blocked_reason": sorted(row["value"] for row in reference.statuses["blocked_reason"]),
        "fixability": sorted(row["value"] for row in reference.statuses["fixability"]),
        "tier": sorted(row["value"] for row in reference.statuses["tier"]),
    }
    actual = {
        "service_type": sorted(props["service_type"]["enum"]),
        "result": sorted(schema["$defs"]["report"]["properties"]["result"]["enum"]),
        "blocked_reason": sorted(schema["$defs"]["report"]["properties"]["blocked_reason"]["enum"]),
        "fixability": sorted(schema["$defs"]["report"]["properties"]["fixability"]["enum"]),
        "tier": sorted(schema["$defs"]["report"]["properties"]["tier"]["enum"]),
    }

    for field, values in expected.items():
        if actual[field] != values:
            only_schema = set(actual[field]) - set(values)
            only_yaml = set(values) - set(actual[field])
            detail = []
            if only_schema:
                detail.append(f"only in schema: {sorted(only_schema)}")
            if only_yaml:
                detail.append(f"only in data/: {sorted(only_yaml)}")
            report.error(
                lib.SCHEMA_PATH,
                f"enum for {field} has drifted from data/: {'; '.join(detail)}",
            )


def check_build(report: Report, entry, index: int, build, reference, today: date) -> None:
    line = entry.key_lines.get("reports")
    match = BUILD_RE.match(str(build))
    if not match:
        return  # the schema pattern already rejected it

    year, month, day = int(match.group(1)), int(match.group(2)), int(match.group(3))
    try:
        parsed = date(year, month, day)
    except ValueError:
        report.error(entry.path, f"report {index}: build {build} has an impossible date", line)
        return

    if parsed > today:
        report.error(entry.path, f"report {index}: build {build} is dated in the future", line)
    elif year < lib.EARLIEST_BUILD_YEAR:
        report.error(
            entry.path,
            f"report {index}: build {build} predates GrapheneOS",
            line,
        )
    elif str(build) not in reference.releases:
        report.warn(
            entry.path,
            f"report {index}: build {build} is not in data/grapheneos-releases.yaml. "
            "That is expected for recent releases; add it if it is missing.",
            line,
        )


def check_entry(report: Report, entry, validator, reference, today: date) -> None:
    meta = entry.meta

    for error in sorted(validator.iter_errors(meta), key=lambda e: list(e.absolute_path)):
        top = error.absolute_path[0] if error.absolute_path else None
        where = ".".join(str(part) for part in error.absolute_path)
        message = f"{where}: {error.message}" if where else error.message
        report.error(entry.path, message, entry.key_lines.get(str(top)) if top else None)

    # A slug that disagrees with its filename breaks the URL and the cross-links.
    if meta.get("slug") and meta["slug"] != entry.slug:
        report.error(
            entry.path,
            f"slug '{meta['slug']}' does not match filename '{entry.slug}.md'",
            entry.key_lines.get("slug"),
        )

    service_type = meta.get("service_type")
    if service_type and service_type not in reference.service_types:
        report.error(
            entry.path,
            f"service_type '{service_type}' is not in data/service-types.yaml",
            entry.key_lines.get("service_type"),
        )

    declared = set(meta.get("countries") or [])
    is_global = bool(meta.get("global"))

    for code in declared:
        if code not in reference.countries:
            report.error(
                entry.path,
                f"country '{code}' is not in data/countries.yaml",
                entry.key_lines.get("countries"),
            )

    if not entry.body.strip():
        report.error(
            entry.path,
            "body is empty. Every app needs a plain-language explanation.",
        )

    reports = meta.get("reports") or []

    # Reports must be newest first, so the top of the file is always current.
    dates = [r.get("date") for r in reports if isinstance(r, dict)]
    if dates != sorted(dates, reverse=True):
        report.error(
            entry.path,
            "reports are not in newest-first order",
            entry.key_lines.get("reports"),
        )

    for index, item in enumerate(reports):
        if not isinstance(item, dict):
            continue
        line = entry.key_lines.get("reports")

        device = item.get("device")
        if device and device not in reference.devices:
            report.error(
                entry.path,
                f"report {index}: device '{device}' is not in data/devices.yaml",
                line,
            )

        code = item.get("country")
        if code and code not in reference.countries:
            report.error(
                entry.path,
                f"report {index}: country '{code}' is not in data/countries.yaml",
                line,
            )
        elif code and not is_global and code not in declared:
            report.error(
                entry.path,
                f"report {index}: country '{code}' is not listed in this app's countries. "
                "Add it there, or set global: true.",
                line,
            )

        raw_date = item.get("date")
        if raw_date:
            try:
                if datetime.strptime(str(raw_date), "%Y-%m-%d").date() > today:
                    report.error(
                        entry.path,
                        f"report {index}: date {raw_date} is in the future",
                        line,
                    )
            except ValueError:
                pass  # the schema already rejected the format

        build = item.get("build")
        if build:
            check_build(report, entry, index, build, reference, today)

        # A fixability verdict that implies instructions, with no instructions.
        if item.get("fixability") in WORKAROUND_REQUIRED and not item.get("workaround"):
            report.error(
                entry.path,
                f"report {index}: fixability is '{item['fixability']}' but workaround is empty",
                line,
            )

        # A blocker recorded against a working result is a contradiction.
        if item.get("result") in {"works", "works-with-setup"} and item.get("blocked_reason") not in {
            "none",
            None,
        }:
            report.warn(
                entry.path,
                f"report {index}: result is '{item['result']}' but blocked_reason is "
                f"'{item['blocked_reason']}'. Usually 'none' is meant.",
                line,
            )


def main() -> int:
    report = Report()
    today = date.today()

    if not lib.SCHEMA_PATH.exists():
        report.error(None, f"missing schema at {lib.SCHEMA_PATH}")
        return 1

    schema = json.loads(lib.SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    reference = lib.load_reference()

    check_enum_drift(report, schema)

    entries, broken = lib.load_entries()
    for path, message in broken:
        report.error(path, message)

    for entry in entries:
        check_entry(report, entry, validator, reference, today)

    total = len(entries) + len(broken)
    if report.errors or report.warnings:
        print()
    print(
        f"{total} entries checked · {report.errors} error(s) · {report.warnings} warning(s)",
        file=sys.stderr,
    )
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
