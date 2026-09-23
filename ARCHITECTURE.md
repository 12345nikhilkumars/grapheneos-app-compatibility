# Architecture

## What this is

A PR-driven markdown repository, built with Hugo, deployed to GitHub Pages. It answers one question: **will my apps work on GrapheneOS, and if not, is it fixable**.

Installation is out of scope.

Every existing resource stops at "this app is broken". None record why it broke or whether it can be fixed, which is the only part a user can act on. The data model is built around those two fields.

## Decisions

| Decision | Value |
|---|---|
| Format | Markdown repo, PR-driven. Issue Forms deferred. |
| Generator | Hugo v0.166.0 extended, pinned in CI |
| Page generation | Hugo content adapters (`_content.gotmpl`) |
| Validation | Python validator against a JSON Schema. Hugo has none. |
| Hosting | GitHub Pages, built by GitHub Actions |
| Code licence | AGPL-3.0-or-later |
| Content licence | CC BY-SA 4.0 |
| Audience | Layered — plain language visible, technical detail collapsed |
| Region | Global-first, India as a first-class country board |
| App URLs | One country-neutral page per app at `/app/<slug>/` |
| Filter matrix | Deferred. JSON feed kept. |
| Search | Client-side, over a build-time JSON index. No dependency. |
| Theming | Light and dark, explicit toggle, `data-theme` on `<html>` |
| v1 scope | Apps only |

## Site structure

```
/                                    Home — board types
/apps/                               Apps — list of countries
/apps/<cc>/                          Country — service types with a status rollup
/apps/<cc>/<service-type>/           Service type — app rows: name, status, why
/app/<slug>/                         App detail — country-neutral
/about/                              What this is
/about/methodology/                  Statuses, trust model, how to read an entry
/about/contribute/                   CONTRIBUTING, rendered
/search-index.json                   Flat app index, fetched on first search
/apps/index.json                     Machine-readable feed
/index.xml                           RSS
```

| URL | Source | Built by |
|---|---|---|
| `/` | hand-written | `content/_index.md` |
| `/apps/` | hand-written intro + generated country list | `content/apps/_index.md` |
| `/apps/<cc>/` | generated | `content/apps/_content.gotmpl` |
| `/apps/<cc>/<type>/` | generated | `content/apps/_content.gotmpl` |
| `/app/<slug>/` | hand-written prose + data frontmatter | `content/app/<slug>.md` |
| `/about/*` | hand-written | `content/about/` |
| `/search-index.json` | generated | `layouts/index.searchindex.json` |

### Board types

Home is a hub of board types. One is built.

| Type | Question it answers | Status |
|---|---|---|
| Apps | Will my apps work, and is it fixable | Built |
| Decide | Should I switch at all | Not built |
| Troubleshoot | Symptom to fix | Not built |
| Devices | Which Pixel to buy | Not built |

### Service types

Thirteen fixed types, listed in `data/service-types.yaml`. A closed list stops the taxonomy sprawling — adding one is a deliberate edit rather than something that happens by accident.

### App page reading order

Layer 1 answers the question in three seconds. The rest is for people who need more. Technical detail collapses with native `<details>`, so the layering costs no JavaScript.

1. **Verdict card** — status, fixability, reason, confidence, last verified
2. **Plain-language summary** — what happens, in two sentences
3. **What to do** — workaround steps, then the alternatives with what each one covers
4. **By country** — status per region
5. *collapsed* — **Technical detail**: reports table, build numbers, devices, profiles
6. *collapsed* — **Contribute**: how to add a report

Most arrivals never see the home page. They come from a search for "does HDFC work on GrapheneOS" and land directly on an app page. Every app page must answer the question without navigation.

## Front end

| Concern | Approach |
|---|---|
| Search | `static/js/site.js` fetches `/search-index.json` once, on first interaction, and ranks matches in the browser. No dependency, no per-keystroke request. |
| Theming | An inline script in `<head>` applies `data-theme` before first paint, so there is no flash. CSS keys off `:root[data-theme="dark"]`, with a `prefers-color-scheme` block for readers without JavaScript. |
| Result links | Arrow keys move real focus between real links. No `aria-activedescendant` simulation. |
| Without JavaScript | Everything structural still works. Search and the theme toggle are the only losses, and the system colour scheme is still honoured. |

The theme's dark token block is written twice — once for the explicit attribute, once behind the media query. The duplication is deliberate: `light-dark()` would express it once, but a browser without support would render an unstyled page rather than the light theme.

## Pipeline

Three stages, each with one job.

```
content/app/<slug>.md          contributor-facing. frontmatter = data, body = prose.
        │
        ▼
scripts/validate.py            schema and cross-reference checks. Fails the build.
        │
        ▼
scripts/build_data.py          derives verdicts, writes data/derived/apps.json
        │
        ▼
content/apps/_content.gotmpl   reads the derived JSON, adds country and type pages
        │
        ▼
hugo --minify                  renders everything
```

Derivation happens in Python, once. The adapter and the layouts both read its output, so a verdict is never computed two different ways.

`data/derived/` is gitignored. `./dev` and CI both regenerate it.

JSON output templates delegate to a partial that calls `return`, because a template's own whitespace would otherwise land in the file. The search index is fetched on every search, so the difference is worth having.

## Data model

One markdown file per app at `content/app/<slug>.md`.

```yaml
---
title: HDFC Bank
slug: hdfc-bank
package: com.hdfcbank.android.now
developer: HDFC Bank
service_type: banking
countries: [IN]
requires_play_services: true
links:
  homepage: https://www.hdfcbank.com
  play_store: https://example.com
  fdroid: null
alternatives:
  - kind: browser
    label: HDFC net banking in a browser
    covers: partial
    detail: Balances, transfers, statements, card controls.
    limitation: No UPI. The website cannot scan a QR code or send a VPA payment.
    url: https://www.hdfcbank.com/
reports:
  - date: 2026-08-14
    build: "2026081200"
    device: pixel-8
    profile: owner
    country: IN
    carrier: Airtel
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: not-possible
    workaround: null
    tier: community
    reporter: "@handle"
---
```

`countries` lists where the app is relevant. Globally available apps set `global: true` instead, so adding a country board does not require editing every global app.

`alternatives` sits on the entry rather than on a report, because what an alternative covers does not change with the OS build. A bank's website exists whether or not the app installs.

### Enums

| Field | Values |
|---|---|
| `result` | `works` · `works-with-setup` · `works-degraded` · `broken` · `unavailable` · `unknown` |
| `blocked_reason` | `play-integrity` · `safetynet` · `custom-firmware-detection` · `hardware-attestation` · `drm` · `play-services-required` · `push-delivery` · `carrier-provisioning` · `none` · `unknown` |
| `fixability` | `not-applicable` · `not-possible` · `possible-with-steps` · `possible-via-workaround` · `unknown` |
| `tier` | `maintainer` · `trusted` · `community` · `imported` |
| `alternatives[].kind` | `browser` · `app` · `hardware` · `phone` · `in-person` · `other` |
| `alternatives[].covers` | `full` · `partial` |

`blocked_reason` and `fixability` are the fields no comparable resource has. `covers` is the field that keeps the alternatives honest.

Every enum is declared twice — in `data/statuses.yaml` for display, and in the schema for validation. JSON Schema cannot read YAML, so `validate.py` asserts the two lists are identical and fails the build if they drift.

### Nullable fields

`build`, `device`, `profile`, `play` and `reporter` are required for first-hand reports and optional for `imported` ones. The schema expresses this with `if`/`then`: tier `imported` requires `source`, every other tier requires `reporter`.

This exists so an imported report can cite a forum post that never stated a build number without inventing one. A guessed build looks like evidence and is worse than a blank field.

### Derived at build time

Never authored — an authored verdict drifts away from the reports it claims to summarise.

| Value | Rule |
|---|---|
| `verdict(app, country)` | Newest report's `result`. Conflicts are surfaced, not hidden. |
| `confidence` | Count of reports in the last 180 days agreeing with the verdict. |
| `last_verified` | Newest report date. |
| `stale` | `last_verified` older than `params.staleAfterDays`. |
| `tier` | Highest tier among agreeing reports. `imported` ranks lowest. |

## Trust model

Four mechanisms, layered. They cover different failure modes.

1. **Dated, versioned, expiring.** Every report carries a date, a GrapheneOS build and a device. A monthly job opens one pinned issue listing everything past the staleness threshold, grouped by country.
2. **Confidence from report count.** Binary result plus a count, never an average — averaging two conflicting reports describes neither. Displayed as "3 reports agree · latest 2026-08-14".
3. **Four-tier verification.** `maintainer` and `trusted` mean a named reviewer reproduced it. `community` means one unverified report. `imported` means nobody here has run it at all.
4. **Source per claim.** An imported report links to the public post it came from, so a reader can check it rather than trust the summary.

**No bare status anywhere.** Every verdict shows status, report count, last-verified date and tier. A status without provenance is a claim, not information.

## CI

| Workflow | Trigger | Does |
|---|---|---|
| `build.yml` | every PR and push | validate, derive, build |
| `deploy.yml` | push to `main` | build and publish to Pages |
| `link-check.yml` | weekly | crawl the built site for dead links |
| `staleness.yml` | monthly | open or update one pinned issue listing stale entries |

`validate.py` checks required fields, enum membership, ISO 3166-1 country codes, service types present in `data/service-types.yaml`, device slugs present in `data/devices.yaml`, build numbers matching `data/grapheneos-releases.yaml`, date format, and no future dates. Failures report as annotations on the offending file.

It also enforces editorial invariants the schema cannot express:

- A `not-possible` or `possible-via-workaround` verdict with nothing under `alternatives`.
- A blocker recorded against a result of `works`.
- `result: broken` with `fixability: not-applicable`.
- `result: broken` with `blocked_reason: none`.

This exists because Hugo performs no validation of its own. Without it, a malformed contribution renders as a blank field rather than failing the build.

## Known gaps

Ranked by how much a reader is misled by the omission.

| Gap | Why it matters |
|---|---|
| Work device management | Microsoft Intune cannot create a work profile, and Microsoft Authenticator has been reported moving to block GrapheneOS. Corporate users are excluded with no warning. |
| Government identity outside India | Only DigiLocker is listed, and it has no reports. myGov, gov.br, Singpass, SwissID, SPID and MyNumber are all uncovered. |
| Banking authenticators | TD Authenticate, Denmark's MitID, Germany's TK-App. These lock people out of accounts they already hold, which is worse than an app not installing. |
| Ride-hailing | Uber runs a Play Integrity check and the driver app is reported broken on custom ROMs. |
| eSIM and VoWiFi | Provisioning failures are a recurring complaint and nothing covers them. |
| Streaming beyond Netflix | Disney+, Prime Video and HBO all degrade under the same DRM mechanics. |
| Games with anti-cheat | The main gaming failure mode, uncovered. |

Adding these is a matter of sourcing them properly. Several were identified during a review of the seed data and deliberately not added, because an entry with a fabricated citation is worse than no entry.

## Open questions

- Repository name, and whether a custom domain is wanted.
- Who reviews pull requests. Review capacity determines what `maintainer` and `trusted` are worth.
- Staleness threshold — currently 180 days, possibly per service type.
- India UPI status is contested. Forum threads report Google Pay stopped, Paytm and BHIM blocking custom firmware, and PhonePe flagging accounts; one third-party guide claims they all work, but that source is machine-generated. The Indian payment entries currently rest on a small number of forum posts. Nothing confident should be published about India UPI until it is tested by hand.
- Whether a country page with one app is worth generating. Adding a bank that operates across Europe currently creates nine near-empty boards.
- Migration content is out of scope and is the largest gap in every existing resource.
