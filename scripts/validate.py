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

    Duplication is unavoidable (JSON Schema cannot read YAML), so it is turned
    into a checked invariant instead of a silent trap. Adding a value to
    statuses.yaml and forgetting the schema (or the reverse) fails the build.
    """
    reference = lib.load_reference()
    props = schema["properties"]
    report_def = schema["$defs"]["report"]["properties"]
    alt_def = schema["$defs"]["alternative"]["properties"]

    pairs = [
        ("service_type", reference.service_types, props["service_type"]["enum"]),
        ("result", reference.statuses["result"], report_def["result"]["enum"]),
        ("blocked_reason", reference.statuses["blocked_reason"], report_def["blocked_reason"]["enum"]),
        ("fixability", reference.statuses["fixability"], report_def["fixability"]["enum"]),
        ("tier", reference.statuses["tier"], report_def["tier"]["enum"]),
        ("profile", reference.statuses["profile"], report_def["profile"]["enum"]),
        ("alternative_kind", reference.statuses["alternative_kind"], alt_def["kind"]["enum"]),
        ("alternative_covers", reference.statuses["alternative_covers"], alt_def["covers"]["enum"]),
    ]

    for field, source, schema_enum in pairs:
        # service_types is keyed by slug; the status files are lists of rows.
        expected = sorted(source) if isinstance(source, dict) else sorted(row["value"] for row in source)
        # A nullable enum carries null beside its real values. Null is the absence
        # of a value rather than one of them, so it has no row in data/ and is
        # dropped here instead of being represented by a placeholder entry.
        actual = sorted(value for value in schema_enum if value is not None)
        if actual == expected:
            continue

        detail = []
        only_schema = set(actual) - set(expected)
        only_yaml = set(expected) - set(actual)
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
    alternatives = meta.get("alternatives") or []

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
        # 'works-with-setup' is excluded on purpose: it means the app runs but
        # only after working around something, so a blocker is expected there.
        if item.get("result") == "works" and item.get("blocked_reason") not in {
            "none",
            None,
        }:
            report.warn(
                entry.path,
                f"report {index}: result is '{item['result']}' but blocked_reason is "
                f"'{item['blocked_reason']}'. Usually 'none' is meant.",
                line,
            )

        # The mirror image: nothing to fix, but the app does not work.
        if item.get("result") in {"broken", "unavailable"} and item.get("fixability") == "not-applicable":
            report.warn(
                entry.path,
                f"report {index}: result is '{item['result']}' but fixability is "
                "'not-applicable'. 'not-applicable' means the app works.",
                line,
            )

        # A working app with something to fix is almost always a mis-set field.
        if item.get("result") == "works" and item.get("fixability") not in {"not-applicable", None}:
            report.warn(
                entry.path,
                f"report {index}: result is 'works' but fixability is "
                f"'{item['fixability']}'. If it works unaided, use 'not-applicable'.",
                line,
            )

        # Claiming no blocker while reporting a failure loses the most useful
        # field on the entry.
        if item.get("result") in {"broken", "unavailable"} and item.get("blocked_reason") == "none":
            report.warn(
                entry.path,
                f"report {index}: result is '{item['result']}' but blocked_reason is "
                "'none'. Use 'unknown' if the cause is not established.",
                line,
            )

    check_alternatives(report, entry, alternatives)


def check_alternatives(report: Report, entry, alternatives: list) -> None:
    """An app the reader cannot use needs somewhere to go.

    The point of the board is not only to say what is broken but to say what to
    do instead. A verdict of 'not-possible' or 'use an alternative' with nothing
    listed under alternatives leaves the reader exactly where they started.
    """
    if alternatives:
        seen = set()
        for index, item in enumerate(alternatives):
            if not isinstance(item, dict):
                continue
            label = item.get("label")
            if label and label.lower() in seen:
                report.warn(
                    entry.path,
                    f"alternative {index}: '{label}' is listed more than once",
                    entry.key_lines.get("alternatives"),
                )
            if label:
                seen.add(label.lower())
        return

    line = entry.key_lines.get("reports")
    for index, item in enumerate(entry.meta.get("reports") or []):
        if not isinstance(item, dict):
            continue
        fixability = item.get("fixability")
        if fixability == "possible-via-workaround":
            report.warn(
                entry.path,
                f"report {index}: fixability is 'possible-via-workaround' but nothing is "
                "listed under alternatives. Name the alternative so the reader can act on it.",
                line,
            )
        elif fixability == "not-possible":
            report.warn(
                entry.path,
                f"report {index}: fixability is 'not-possible' but nothing is listed under "
                "alternatives. Even an unfixable app usually has a fallback: a website, "
                "another app, or a physical card.",
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
