# Contributing

Two things get contributed here: **new reports** on apps that already have an entry, and **new app entries**. Both are pull requests.

## The one rule

**Test it yourself.** A report is a claim about what happened on a real device running a real GrapheneOS build. If you have not run the app on GrapheneOS, do not submit a report about it.

Do not submit AI-generated reports, or reports assembled from other people's forum posts. This project exists because the existing resources are full of unverified claims and machine-written SEO pages. A single fabricated entry damages the whole board more than an empty one does. Pull requests that fail this rule are closed without discussion.

An entry with **no reports at all** is a valid and useful state. It says the app matters and nobody has tested it. Do not fill that gap with a guess.

## Adding a report to an existing app

1. Open `content/app/<app-slug>.md`.
2. Add an entry to the top of the `reports` list, newest first.
3. Open a pull request.

```yaml
reports:
  - date: 2026-08-14          # the day you tested. Not the day you are writing this.
    build: "2026081200"       # the exact GrapheneOS release you were running
    device: pixel-8           # from data/devices.yaml
    profile: owner            # owner | secondary
    country: IN               # ISO 3166-1 alpha-2. Where the app was used.
    carrier: Airtel           # only if the failure is carrier-related, else omit
    play: sandboxed           # sandboxed | microg | none
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: not-possible
    workaround: null
    tier: community
    reporter: "@yourhandle"
```

Every field above except `carrier`, `workaround` and `source` is required for a first-hand report. `source` must be absent: a report carrying a `source` is second-hand by definition, and will be rejected.

### Getting `result` right

| Value | Use it when |
|---|---|
| `works` | Runs normally, no setup beyond installing it. |
| `works-with-setup` | Runs, but only after you changed something. Say what in `workaround`. |
| `works-degraded` | Runs, but a feature is missing or capped. |
| `broken` | Installs, but is unusable. Refuses to start, or cannot do its main job. |
| `unavailable` | Cannot be installed at all. |
| `unknown` | You could not tell. Rare; prefer one of the above. |

The distinction that matters most is `works` versus `works-with-setup`. If you had to toggle a setting to get there, it is `works-with-setup`, and the toggle belongs in `workaround`. If it worked unaided, `fixability` is `not-applicable`. Do not record a workaround for an app that needed none.

### Getting `blocked_reason` right

Only set it if you actually know why it failed. If the app refused to start and you have no idea why, use `unknown`. A wrong reason is worse than an honest gap: it sends the next person down a path that cannot work.

If you do know, the tell-tale signs:

| What you saw | Likely `blocked_reason` |
|---|---|
| Fails an integrity check despite a locked bootloader | `play-integrity` |
| Names "custom firmware", "modified system", or similar | `custom-firmware-detection` |
| Demands Play Services and will not run without them | `play-services-required` |
| Protected video is capped at low resolution | `drm` |
| Notifications arrive late or never | `push-delivery` |
| Fails only on mobile data, works on Wi-Fi | `carrier-provisioning` |

Note on `drm`: a resolution cap usually means the Widevine provisioning path is broken, **not** that Widevine L1 is unavailable. GrapheneOS does support L1 on Pixels. Check whether it is a provisioning problem before recording it as permanent.

### Getting `fixability` right

This is the field people come here for.

- `not-applicable`: the app works. There is nothing to fix.
- `not-possible`: no known workaround, and none is plausible. Be sure before using this. Reserve it for a check that is deliberate and enforced server-side.
- `possible-with-steps`: works if you change something first. Put the steps in `workaround`.
- `possible-via-workaround`: the app itself cannot work, but an alternative can do the same job. Name it in `workaround`, and add it to `alternatives` (below).
- `unknown`: nobody has tried yet.

## Alternatives

An app the reader cannot use needs somewhere to go. `alternatives` is a top-level field on the entry, not part of a report, because what an alternative covers does not change with the OS build: a bank's website exists whether or not the app installs.

Add one whenever `fixability` is `not-possible` or `possible-via-workaround`. Validation warns if you do not.

```yaml
alternatives:
  - kind: browser            # browser | app | hardware | phone | in-person | other
    label: HDFC net banking in a browser
    covers: partial          # full | partial
    detail: "What it does, in plain language."
    limitation: "What it does not do. Required when covers is partial."
    url: https://www.hdfcbank.com/
```

**`covers` is the field that matters.** "Use the website instead" is misleading when the website cannot make a payment. If the alternative covers most of the job but not the part people actually need, that is `partial`, and `limitation` has to say what is lost.

The HDFC entry is the worked example: browser net banking restores account access but gives you no UPI, and UPI is the reason most people open the app. That gap is the single most useful sentence on the page.

## Adding a new app

1. Copy an existing file in `content/app/` as a template.
2. Set `service_type` from `data/service-types.yaml` and `countries` from `data/countries.yaml`. Globally available apps use `global: true` instead of `countries`.
3. Write the body in plain language first. What the app is, what happens on GrapheneOS, what to do about it. Assume the reader is not technical.
4. Add `alternatives` if there is any fallback worth knowing about.
5. Run `./dev`. It will tell you if anything is wrong.
6. Open a pull request.

**Source every claim.** If a sentence states a fact about an app's behaviour, it should be something you tested or something you can link to. The board has been burned by this: entries have carried source links to forum threads that did not mention the app in question. A claim with no source and no test behind it does not belong in the entry.

## Trust tiers

Every report carries a `tier`. It is shown on the site, so readers can weigh what they are reading.

| Tier | Meaning |
|---|---|
| `community` | One person's report, not reproduced. This is the default and it is fine. |
| `trusted` | A trusted contributor reproduced it independently. |
| `maintainer` | Reproduced and confirmed by a maintainer. |
| `imported` | Taken from a public source rather than tested by anyone here. |

Do not set your own report above `community`. Tiers are raised during review, and only after someone else has reproduced the result.

### Imported reports

`imported` is for maintainers seeding an entry from a public source: a forum thread, an issue, a news report. It is not something to submit in a pull request.

An imported report **must** carry a `source`, and it may leave `build`, `device`, `profile` and `play` empty. That is deliberate. Forcing an imported report to name a build the original author never stated would mean inventing one, and a fabricated build number is worse than an empty field. Leave it null.

Imported reports rank below `community` when the site works out how much agreement a verdict has. They are a lead, not a finding.

## What a maintainer will check

- That the report reads as first-hand, and carries no `source`
- That `build` is a real GrapheneOS release, or null on an imported report
- That `date` is not in the future and not implausibly old
- That enums are valid and cross-references resolve
- That a `not-possible` or `possible-via-workaround` verdict has something under `alternatives`
- That no unrelated entries were changed

## Running the checks locally

```sh
./dev                          # validate, derive, and serve
uv run --project scripts python scripts/validate.py   # validation only
```

CI runs the same commands. If `./dev` passes locally, the build should pass.

## Licence

By contributing you agree to your prose and data being published under CC BY-SA 4.0, and any code under AGPL-3.0-or-later.
