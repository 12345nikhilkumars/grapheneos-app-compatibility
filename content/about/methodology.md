---
title: Methodology
---

How a status gets on this site, and how much you should trust it.

## The three fields that matter

Every app carries three things, and the third is the one nobody else publishes.

| Field | Question |
|---|---|
| **Status** | Did it work |
| **Why** | What stopped it |
| **Fixability** | Is there a way around it |

A status on its own — "broken" — tells you nothing you can act on. "Broken because the app performs its own firmware check, and no workaround exists" tells you to stop trying. That distinction is the entire point of this board.

## Statuses

| Status | Meaning |
|---|---|
| **Works** | Runs normally with no setup beyond installing it. |
| **Works with setup** | Runs, but only after a change — sandboxed Play Services, an exploit-protection exception, a settings toggle. |
| **Works, degraded** | Runs, but a feature is missing or capped. Usually DRM resolution or push notifications. |
| **Broken** | Installs, but is unusable. Refuses to start, fails an integrity check, or cannot complete its main task. |
| **Unavailable** | Cannot be installed at all. |
| **Unknown** | Nobody has reported testing it in this country. |

**Unknown is the honest default, not a failure.** Where no one has reported from your country, the app shows as unknown rather than inheriting a result from somewhere else. The apps that fail most often are country-specific, so borrowing a verdict across borders would be misleading.

## Why an app fails

Only set when the reporter actually knows. A wrong reason is worse than an honest gap, because it sends the next person down a path that cannot work.

| Reason | What it means |
|---|---|
| Play Integrity | The app checks Play Integrity and fails. Locking the bootloader does not help. |
| SafetyNet | The older attestation API. Same failure, older mechanism. |
| Custom firmware detection | The app notices the OS is not stock and refuses, without naming an API. |
| Hardware attestation | Fails a hardware-backed key attestation. Not bypassable. |
| DRM | Widevine L3 only, so protected video is capped at low resolution. |
| Play Services required | Will not run without Google Play Services. |
| Push delivery | Notifications arrive late or never. Usually a battery-optimisation problem. |
| Carrier provisioning | The carrier has not provisioned the device. Usually VoLTE, VoWiFi or eSIM. |

## Fixability

| Verdict | Meaning |
|---|---|
| **Nothing to fix** | The app works. |
| **Not fixable** | No workaround exists, and none is plausible. |
| **Fixable with steps** | Works if you change something first. The steps are listed. |
| **Use an alternative** | The app cannot work, but another app can do the same job. |
| **Unknown** | Nobody has tried yet. This is not the same as not fixable. |

The difference between **not fixable** and **unknown** matters more than any other distinction here. `Not fixable` means stop looking. `Unknown` means you might be the person who finds out.

## How a verdict is derived

Verdicts are computed at build time from the reports. They are never written by hand, because a hand-written verdict drifts away from the reports it claims to summarise.

- **The verdict is the newest report's result.** Not an average. Averaging two conflicting reports produces a value that describes neither of them.
- **Confidence is the number of recent reports that agree.** Shown as "3 reports agree".
- **Dissent is counted, not hidden.** If recent reports disagree with the verdict, that is displayed rather than smoothed away.
- **Last verified is the newest report date**, and it is always shown.

## Staleness

An entry whose newest report is more than 180 days old is marked as possibly out of date. A monthly job collects them into one issue.

GrapheneOS ships every few days, and app behaviour changes with it. A verdict from a year ago is a historical claim, not a current one. Treat it accordingly.

## Who verified it

| Tier | Meaning |
|---|---|
| **Community report** | One person's report. Not reproduced. This is the default, and it is fine. |
| **Verified by contributor** | Independently reproduced by a trusted contributor. |
| **Verified by maintainer** | Reproduced and confirmed by a maintainer. |

## Imported reports

Some entries were seeded from public forum threads and issue trackers rather than tested by a contributor to this project. Those reports carry a link to their source and are labelled as imported.

**Imported reports have not been reproduced.** They are a starting point, not a finding. Contributors are not permitted to submit them — if you have not run the app yourself, it does not belong here.

This distinction exists because the alternative — quietly presenting second-hand information as tested — is precisely the failure this project was built to avoid.

## What this site does not claim

- That GrapheneOS is secure, or that any device is.
- That an app listed as working is safe, or respects your privacy. Functional and trustworthy are different questions.
- That a status is current. Check the date on every entry before relying on it.

Nothing here is affiliated with the GrapheneOS project.
