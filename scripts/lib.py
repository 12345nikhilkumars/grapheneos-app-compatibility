"""Shared loading helpers for the Info Board tooling.

Nothing here validates. validate.py owns correctness, build_data.py owns
derivation. Both read through these helpers so they agree on what a file is.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
CONTENT_APP = ROOT / "content" / "app"
DATA_DIR = ROOT / "data"
DERIVED_DIR = DATA_DIR / "derived"
SCHEMA_PATH = ROOT / "schemas" / "app.schema.json"

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


class Loader(yaml.SafeLoader):
    """SafeLoader with the timestamp resolver removed.

    PyYAML turns an unquoted `2026-09-10` into a datetime.date, which then
    fails JSON Schema string validation and cannot be serialised. Contributors
    should not have to remember to quote every date, so the conversion is
    disabled and dates stay as the strings they were written as.
    """


Loader.yaml_implicit_resolvers = {
    key: [(tag, regexp) for tag, regexp in mappings if tag != "tag:yaml.org,2002:timestamp"]
    for key, mappings in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

# How far back a build string may plausibly point. GrapheneOS began in 2019.
EARLIEST_BUILD_YEAR = 2019

# A verdict only counts as current if it was confirmed within this window.
STALE_AFTER_DAYS = 180

# Most severe first. Drives sort order so broken apps surface at the top.
RESULT_SEVERITY = {
    "broken": 0,
    "unavailable": 1,
    "works-degraded": 2,
    "works-with-setup": 3,
    "works": 4,
    "unknown": 5,
}

TIER_RANK = {"maintainer": 3, "trusted": 2, "community": 1}


class EntryError(Exception):
    """A file could not be read as an entry at all."""


@dataclass(frozen=True)
class Entry:
    path: Path
    slug: str
    meta: dict
    body: str
    key_lines: dict[str, int]


def load_yaml(path: Path):
    with path.open(encoding="utf-8") as handle:
        return yaml.load(handle, Loader=Loader)


def parse_frontmatter(path: Path) -> Entry:
    """Read an app file into metadata plus body.

    Deliberately hand-rolled rather than pulling in python-frontmatter: the
    format is a delimiter, a YAML block, a delimiter. That is not worth a
    dependency.
    """
    text = path.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        raise EntryError("no YAML frontmatter delimited by ---")

    raw = match.group(1)
    try:
        meta = yaml.load(raw, Loader=Loader)
    except yaml.YAMLError as exc:
        raise EntryError(f"frontmatter is not valid YAML: {exc}") from exc

    if not isinstance(meta, dict):
        raise EntryError("frontmatter must be a mapping")

    key_lines: dict[str, int] = {}
    for offset, line in enumerate(raw.splitlines()):
        found = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):", line)
        if found:
            key_lines.setdefault(found.group(1), offset + 2)

    return Entry(
        path=path,
        slug=path.stem,
        meta=meta,
        body=text[match.end():].strip(),
        key_lines=key_lines,
    )


def load_entries() -> tuple[list[Entry], list[tuple[Path, str]]]:
    """Return every app entry, plus the files that could not be parsed."""
    entries: list[Entry] = []
    broken: list[tuple[Path, str]] = []
    for path in sorted(CONTENT_APP.glob("*.md")):
        try:
            entries.append(parse_frontmatter(path))
        except EntryError as exc:
            broken.append((path, str(exc)))
    return entries, broken


@dataclass(frozen=True)
class Reference:
    countries: dict[str, dict]
    service_types: dict[str, dict]
    devices: dict[str, dict]
    releases: dict[str, dict]
    statuses: dict


def load_reference() -> Reference:
    countries = {row["code"]: row for row in load_yaml(DATA_DIR / "countries.yaml")}
    service_types = {row["slug"]: row for row in load_yaml(DATA_DIR / "service-types.yaml")}
    devices = {row["slug"]: row for row in load_yaml(DATA_DIR / "devices.yaml")}
    releases = {row["build"]: row for row in load_yaml(DATA_DIR / "grapheneos-releases.yaml")}
    statuses = load_yaml(DATA_DIR / "statuses.yaml")
    return Reference(countries, service_types, devices, releases, statuses)
