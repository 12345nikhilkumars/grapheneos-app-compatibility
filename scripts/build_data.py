#!/usr/bin/env python3
"""Derive per-country verdicts and write data/derived/apps.json.

Derivation lives here and only here. The Hugo content adapter and the layouts
both read this output, so a verdict is never computed two different ways.

Nothing in this file is authored by hand. Authored verdicts drift away from the
reports they claim to summarise, which is the failure mode this whole project
exists to avoid.
"""

from __future__ import annotations

import json
import sys
from datetime import date, timedelta

import lib
from lib import RESULT_SEVERITY, STALE_AFTER_DAYS, TIER_RANK

UNREPORTED = {
    "reported": False,
    "verdict": "unknown",
    "fixability": "unknown",
    "blocked_reason": "unknown",
    "confidence": 0,
    "dissent": 0,
    "last_verified": None,
    "stale": False,
    "tier": None,
    "latest": None,
}


def parse_date(value):
    try:
        return date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None


def derive(reports: list[dict], code: str, cutoff: date) -> dict:
    """Fold every report for one country into a single verdict.

    The verdict is the newest report's result, not an average. Averaging two
    conflicting reports produces a value that describes neither of them.
    Dissent is counted and surfaced rather than smoothed away.
    """
    local = [row for row in reports if row.get("country") == code]
    if not local:
        return dict(UNREPORTED)

    local = sorted(local, key=lambda row: str(row.get("date")), reverse=True)
    latest = local[0]
    verdict = latest.get("result", "unknown")

    recent = [row for row in local if (parse_date(row.get("date")) or date.min) >= cutoff]
    agree = [row for row in recent if row.get("result") == verdict]
    dissent = [row for row in recent if row.get("result") != verdict]

    tier = max(
        (row.get("tier") for row in agree),
        key=lambda value: TIER_RANK.get(value, 0),
        default=latest.get("tier"),
    )
    last_verified = max(str(row.get("date")) for row in local)

    return {
        "reported": True,
        "verdict": verdict,
        "fixability": latest.get("fixability", "unknown"),
        "blocked_reason": latest.get("blocked_reason", "unknown"),
        "confidence": len(agree),
        "dissent": len(dissent),
        "last_verified": last_verified,
        "stale": (parse_date(last_verified) or date.min) < cutoff,
        "tier": tier,
        "latest": latest,
    }


def main() -> int:
    reference = lib.load_reference()
    entries, broken = lib.load_entries()

    if broken:
        print(
            "refusing to derive: some entries could not be parsed. Run validate.py.",
            file=sys.stderr,
        )
        return 1

    today = date.today()
    cutoff = today - timedelta(days=STALE_AFTER_DAYS)

    # Which countries get a page: any an app explicitly declares, plus any a
    # report was filed from. A globally available app does not by itself
    # justify a page for every country.
    declared: set[str] = set()
    for entry in entries:
        if not entry.meta.get("global"):
            declared.update(entry.meta.get("countries") or [])
        for row in entry.meta.get("reports") or []:
            if isinstance(row, dict) and row.get("country"):
                declared.add(row["country"])

    apps: dict[str, dict] = {}
    report_count = 0

    for entry in entries:
        meta = entry.meta
        reports = meta.get("reports") or []
        report_count += len(reports)

        is_global = bool(meta.get("global"))
        own = sorted(meta.get("countries") or [])
        codes = sorted(declared) if is_global else own

        apps[entry.slug] = {
            "slug": entry.slug,
            "title": meta["title"],
            "service_type": meta["service_type"],
            "developer": meta.get("developer"),
            "package": meta.get("package"),
            "links": meta.get("links") or {},
            "countries": own,
            "global": is_global,
            "requires_play_services": bool(meta.get("requires_play_services")),
            "alternatives": meta.get("alternatives") or [],
            "by_country": {code: derive(reports, code, cutoff) for code in codes},
            "reports": reports,
        }

    countries_out = []
    for code in sorted(declared):
        info = reference.countries.get(code)
        if info is None:
            continue

        types_out = []
        for service_type in sorted(reference.service_types.values(), key=lambda row: row["order"]):
            rows = []
            for app in apps.values():
                if app["service_type"] != service_type["slug"]:
                    continue
                if not (app["global"] or code in app["countries"]):
                    continue
                derived = app["by_country"].get(code)
                if derived is None:
                    continue
                rows.append(
                    {
                        "slug": app["slug"],
                        "title": app["title"],
                        "developer": app["developer"],
                        "requires_play_services": app["requires_play_services"],
                        **{k: v for k, v in derived.items() if k != "latest"},
                    }
                )

            if not rows:
                continue

            # Most broken first, so problems surface before successes.
            rows.sort(key=lambda row: (RESULT_SEVERITY.get(row["verdict"], 99), row["title"].lower()))

            counts: dict[str, int] = {}
            for row in rows:
                counts[row["verdict"]] = counts.get(row["verdict"], 0) + 1

            types_out.append(
                {
                    "slug": service_type["slug"],
                    "label": service_type["label"],
                    "note": service_type.get("note"),
                    "total": len(rows),
                    # How many of these anyone has actually reported on. The
                    # difference between "11 apps" and "11 apps, 2 tested" is the
                    # difference between coverage and the appearance of it.
                    "reported": sum(1 for row in rows if row["reported"]),
                    "counts": counts,
                    "apps": rows,
                }
            )

        if not types_out:
            continue

        # Country totals are counts, not a verdict. A country is a container, not
        # something that can work or break: a single failing app must not be
        # rendered as "this country is broken". Nor may an untested country be
        # rendered as working, which is what a worst-of badge defaulting to
        # "works" did for every country with no reports at all. There is
        # deliberately no "worst" key here for a template to reach for.
        country_counts: dict[str, int] = {}
        for item in types_out:
            for value, n in item["counts"].items():
                country_counts[value] = country_counts.get(value, 0) + n

        countries_out.append(
            {
                "code": code,
                "name": info["name"],
                "region": info["region"],
                "order": info["order"],
                "priority": bool(info.get("priority")),
                "total": sum(item["total"] for item in types_out),
                "reported": sum(item["reported"] for item in types_out),
                "counts": country_counts,
                "types": types_out,
            }
        )

    countries_out.sort(key=lambda row: (not row["priority"], row["region"], row["order"], row["code"]))

    payload = {
        "generated": today.isoformat(),
        "stale_after_days": STALE_AFTER_DAYS,
        "country_codes": sorted(declared),
        "service_types": sorted(reference.service_types.values(), key=lambda row: row["order"]),
        "apps": apps,
        "countries": countries_out,
        "summary": {
            "apps": len(apps),
            "countries": len(countries_out),
            "reports": report_count,
            "stale": sum(
                1
                for app in apps.values()
                for derived in app["by_country"].values()
                if derived["stale"]
            ),
        },
    }

    lib.DERIVED_DIR.mkdir(parents=True, exist_ok=True)
    out = lib.DERIVED_DIR / "apps.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    summary = payload["summary"]
    print(
        f"derived {summary['apps']} apps · {summary['countries']} country pages · "
        f"{summary['reports']} reports · {summary['stale']} stale verdict(s)",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
