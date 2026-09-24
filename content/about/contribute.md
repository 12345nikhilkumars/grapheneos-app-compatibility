---
title: Contribute
---

Everything on this site is a markdown file in a public repository, and every change is a pull request.

## There is only one rule

**Test it yourself.** A report is a claim about what happened on a real device running a real GrapheneOS build. If you have not run the app, do not submit a report about it.

Do not submit second-hand reports, and do not submit anything written by a language model. This project exists because the existing resources are full of unverified claims and machine-written pages. One fabricated entry does more damage than an empty one.

## Adding a report

Open `content/app/<slug>.md` and add an entry to the top of the `reports` list.

```yaml
reports:
  - date: 2026-09-10          # the day you tested, not the day you are writing
    build: "2026091000"       # the GrapheneOS release you were running
    device: pixel-8           # from data/devices.yaml
    profile: owner            # owner | secondary
    country: IN               # where the app was used
    play: sandboxed           # sandboxed | microg | none
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: not-possible
    workaround: null
    tier: community
    reporter: "@yourhandle"
```

Then run `./dev` and open a pull request.

## Adding an app

Copy an existing file in `content/app/` as a template, set `service_type` and `countries`, and write the body in plain language first. Assume the reader is not technical.

An app with no reports yet is a valid entry. It shows as unknown, which is more useful than a guess.

## Getting the fields right

**`blocked_reason`**: only set it if you know why it failed. A wrong reason is worse than an honest empty field.

| What you saw | Likely reason |
|---|---|
| Fails an integrity check despite a locked bootloader | `play-integrity` |
| Names "custom firmware" or "modified system" | `custom-firmware-detection` |
| Demands Play Services and will not run without them | `play-services-required` |
| Runs, but a feature is capped | `drm` or `push-delivery` |
| Fails only on mobile data, works on Wi-Fi | `carrier-provisioning` |

**`fixability`**: this is the field people come here for. `not-possible` means stop looking. `unknown` means nobody has tried, and you might be the one who finds out. Do not use `not-possible` unless you are sure.

## Trust tiers

Do not set your own report above `community`. Tiers are raised during review, and only after somebody else has reproduced the result.

## Licence

By contributing, you agree to your prose and data being published under CC BY-SA 4.0, and any code under AGPL-3.0-or-later.

## Full guide

The complete contributing guide, including the review checklist, lives in the repository.

[Read CONTRIBUTING.md →](https://github.com/example/grapheneos-info-board/blob/main/CONTRIBUTING.md)
