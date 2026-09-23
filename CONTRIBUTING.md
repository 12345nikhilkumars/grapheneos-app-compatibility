# Contributing

Two things get contributed here: **new reports** on apps that already have an entry, and **new app entries**. Both are pull requests.

## The one rule

**Test it yourself.** A report is a claim about what happened on a real device running a real GrapheneOS build. If you have not run the app on GrapheneOS, do not submit a report about it.

Do not submit AI-generated reports, or reports assembled from other people's forum posts. This project exists because the existing resources are full of unverified claims and machine-written SEO pages. A single fabricated entry damages the whole board more than an empty one does. Pull requests that fail this rule are closed without discussion.

## Adding a report to an existing app

1. Open `content/app/<app-slug>.md`.
2. Add an entry to the top of the `reports` list — newest first.
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

### Getting `blocked_reason` right

Only set it if you actually know why it failed. If the app refused to start and you have no idea why, use `unknown`. A wrong reason is worse than an honest gap — it sends the next person down a path that cannot work.

If you do know, the tell-tale signs:

| What you saw | Likely `blocked_reason` |
|---|---|
| App fails an integrity check despite a locked bootloader | `play-integrity` |
| App names "custom firmware", "modified system", or similar | `custom-firmware-detection` |
| App demands Play Services and will not run without them | `play-services-required` |
| Installs and runs, but a specific feature is capped (video resolution, payments) | `drm` |
| Fails only on one network, works on Wi-Fi | `carrier-provisioning` |

### Getting `fixability` right

This is the field people come here for.

- `not-applicable` — the app works. There is nothing to fix.
- `not-possible` — no known workaround, and none is plausible. Be sure before using this.
- `possible-with-steps` — works if you change something first. Put the steps in `workaround`.
- `possible-via-workaround` — the app itself cannot work, but an alternative can do the same job. Name it in `workaround`.
- `unknown` — nobody has tried yet.

## Adding a new app

1. Copy an existing file in `content/app/` as a template.
2. Set `service_type` from `data/service-types.yaml` and `countries` from `data/countries.yaml`. Globally available apps use `global: true` instead of `countries`.
3. Write the body in plain language first. What the app is, what happens on GrapheneOS, what to do about it. Assume the reader is not technical.
4. Run `./dev`. It will tell you if anything is wrong.
5. Open a pull request.

## Trust tiers

Every report carries a `tier`. It is shown on the site, so readers can weigh what they are reading.

| Tier | Meaning |
|---|---|
| `community` | One person's report, not reproduced. This is the default and it is fine. |
| `trusted` | A maintainer or trusted contributor reproduced it independently. |
| `maintainer` | Reproduced and confirmed by a maintainer. |

Do not set your own report above `community`. Tiers are raised during review, and only after someone else has reproduced the result.

## What a maintainer will check

- That the report reads as first-hand
- That `build` is a real GrapheneOS release
- That `date` is not in the future and not implausibly old
- That enums are valid and cross-references resolve
- That no unrelated entries were changed

## Running the checks locally

```sh
./dev              # validate, derive, and serve
uv run scripts/validate.py   # validation only
```

CI runs the same commands. If `./dev` passes locally, the build should pass.

## Licence

By contributing you agree to your prose and data being published under CC BY-SA 4.0, and any code under AGPL-3.0-or-later.
