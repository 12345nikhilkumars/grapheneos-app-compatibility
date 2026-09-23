#!/usr/bin/env python3
"""Print a markdown report of entries whose verdicts have gone stale.

Run by the monthly staleness workflow, which puts the output into a pinned
issue. Nothing here writes to the repository.
"""

from __future__ import annotations

import json
import sys

import lib


def main() -> int:
    path = lib.DERIVED_DIR / "apps.json"
    if not path.exists():
        print("data/derived/apps.json is missing. Run scripts/build_data.py first.", file=sys.stderr)
        return 1

    data = json.loads(path.read_text(encoding="utf-8"))
    window = data["stale_after_days"]
    generated = data["generated"]

    stale: list[tuple[str, str, str, str]] = []
    for app in data["apps"].values():
        for code, row in app["by_country"].items():
            if row.get("stale"):
                stale.append((app["title"], code, row["last_verified"], row["verdict"]))

    stale.sort(key=lambda item: (item[2], item[0]))

    print(f"# Stale entries as of {generated}")
    print()
    print(f"A verdict is treated as stale once it is more than {window} days old.")
    print("Nothing here is wrong. It is simply old enough that it may no longer be true.")
    print("Re-testing one of these, or confirming it still holds, is a useful contribution.")
    print()

    if not stale:
        print("No entries are stale.")
        return 0

    print(f"**{len(stale)} entries need re-verification.**")
    print()
    print("| App | Country | Last verified | Current verdict |")
    print("| --- | --- | --- | --- |")
    for title, code, last_verified, verdict in stale:
        print(f"| {title} | {code} | {last_verified} | `{verdict}` |")
    print()
    print("To refresh one, run the app on a current build and add a report to")
    print("`content/app/<slug>.md`, then open a pull request.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
