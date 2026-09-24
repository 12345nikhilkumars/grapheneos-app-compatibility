#!/usr/bin/env python3
"""Check every internal link in the built site.

External links are checked weekly by lychee, which needs the network. Internal
links are a different problem: they are generated from data, so a renamed slug,
a country that lost its page, or a typo in a relURL all produce a 404 that only
shows up when someone clicks it. That check costs nothing and belongs in the
build.

Parsed with html.parser rather than a regex, because Hugo's minifier rewrites
`href="/apps/"` to `href=/apps/` and a regex looking for quotes silently finds
nothing and reports success. That mistake was made once already.

Root-relative links carry the site's base path but the output directory does
not. Hugo writes `public/apps/index.html` while the link on the page reads
`/grapheneos-app-compatibility/apps/`. The base path is read from `hugo.toml`
and stripped before resolving. Without that, every internal link reports as
broken the moment the site is served from a project page rather than a domain
root.

Usage:
    scripts/linkcheck.py [directory]      # defaults to public/
"""

from __future__ import annotations

import sys
import tomllib
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

SKIP_SCHEMES = ("http", "https", "mailto", "tel", "data", "javascript")


def site_base_path(root: Path) -> str:
    """The path component of the configured baseURL, e.g. "/sub/" or "/"."""
    for candidate in (root.parent / "hugo.toml", root / "hugo.toml"):
        if not candidate.is_file():
            continue
        try:
            config = tomllib.loads(candidate.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            continue
        path = urlsplit(str(config.get("baseURL", ""))).path
        if path and path != "/":
            return path if path.endswith("/") else path + "/"
    return "/"


class LinkCollector(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.ids: set[str] = set()
        self._anchor_depth = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)

        if tag == "a":
            href = values.get("href")
            if href:
                self.links.append(href)

        # Fragment targets. The skip link and in-page anchors depend on these.
        element_id = values.get("id")
        if element_id:
            self.ids.add(element_id)

        if tag == "a" and values.get("name"):
            self.ids.add(values["name"])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def target_for(root: Path, page: Path, href: str, base_path: str = "/") -> Path | None:
    """Resolve an href to a file on disk, or None if it is not our problem."""
    parts = urlsplit(href)

    if parts.scheme in SKIP_SCHEMES or href.startswith("//"):
        return None
    if parts.scheme and parts.scheme not in ("", "file"):
        return None

    path = unquote(parts.path)
    if not path:
        return None  # pure fragment, handled by the caller

    if path.startswith("/"):
        # Root-relative links are relative to the output directory, not the
        # page. Strip the site's base path first: the deployed site sits under
        # it, but the output directory does not have a matching subdirectory.
        if base_path != "/" and path.startswith(base_path):
            path = "/" + path[len(base_path):]
        directory = root
    else:
        directory = page.parent

    resolved = (directory / path.lstrip("/")).resolve()

    if path.endswith("/"):
        return resolved / "index.html"
    if resolved.is_dir():
        return resolved / "index.html"
    if resolved.suffix:
        return resolved
    return resolved.with_suffix(".html")


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "public").resolve()
    if not root.is_dir():
        print(f"no such directory: {root}", file=sys.stderr)
        return 1

    pages = sorted(root.rglob("*.html"))
    if not pages:
        print(f"no HTML found under {root}. Build first.", file=sys.stderr)
        return 1

    checked = 0
    broken: list[tuple[Path, str, str]] = []
    base_path = site_base_path(root)

    # First pass: collect the ids each page defines, for fragment checking.
    ids_by_page: dict[Path, set[str]] = {}
    collectors: dict[Path, LinkCollector] = {}

    for page in pages:
        collector = LinkCollector()
        collector.feed(page.read_text(encoding="utf-8", errors="replace"))
        collectors[page] = collector
        ids_by_page[page] = collector.ids

    for page in pages:
        for href in collectors[page].links:
            target = target_for(root, page, href, base_path)
            if target is None:
                continue

            checked += 1
            rel_page = page.relative_to(root)

            if not target.exists():
                broken.append((rel_page, href, "no such file"))
                continue

            fragment = urlsplit(href).fragment
            if fragment and target.suffix == ".html":
                defined = ids_by_page.get(target.resolve())
                if defined is not None and fragment not in defined:
                    broken.append((rel_page, href, f"no id '{fragment}' on that page"))

    for page, href, why in broken:
        print(f"broken  {page}: {href}  ({why})")

    print(
        f"\n{checked} internal link(s) across {len(pages)} page(s) · "
        f"{len(broken)} broken",
        file=sys.stderr,
    )
    return 1 if broken else 0


if __name__ == "__main__":
    sys.exit(main())
