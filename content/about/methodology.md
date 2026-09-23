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
| **Works, degraded** | Runs, but a feature is missing or capped. Usually push notifications, or one feature inside an otherwise working app. |
| **Broken** | Installs, but is unusable. Refuses to start, fails an integrity check, or cannot complete its main task. |
| **Unavailable** | Cannot be installed at all. |
| **Unknown** | Nobody has reported testing it in this country. |

**Unknown is the honest default, not a failure.** Where no one has reported from your country, the app shows as unknown rather than inheriting a result from somewhere else. The apps that fail most often are country-specific, so borrowing a verdict across borders would be misleading.

## Why an app fails

Only set when the reporter actually knows. A wrong reason is worse than an honest gap, because it sends the next person down a path that cannot work.

| Reason | What it means |
|---|---|
| Play Integrity | The app calls the Play Integrity API and fails the device or strong integrity verdict. Locking the bootloader does not help. |
| SafetyNet | The older attestation API. Same failure, older mechanism. |
| Custom firmware detection | The app inspects the OS itself and refuses to run, without naming an API. |
| Exploit protection | One of GrapheneOS's own hardening features is what the app trips over, not an attestation check. Usually fixed per app under Settings → Apps → the app → Exploit protection. |
| Hardware attestation | Fails a hardware-backed key attestation against Google's servers. |
| DRM | Protected content is capped at low resolution. Usually a provisioning problem rather than L1 being unavailable — GrapheneOS supports Widevine L1 on Pixels. |
| Play Services required | Will not run without Google Play Services. |
| Push delivery | Notifications arrive late or never. Usually battery optimisation suspending sandboxed Play Services. |
| Carrier provisioning | The carrier has not provisioned the device. Usually VoLTE, VoWiFi or eSIM. |

## Exploit protection, and what the workarounds cost

Some apps fail on GrapheneOS not because they reject the operating system but because one of its own hardening features breaks them. That is a different problem with a different answer, so it has its own reason code. It also has a price, and this site will not tell you to pay it without saying what it is.

| Setting | Where | What it costs |
|---|---|---|
| **Native code debugging** | Settings → Apps → the app → Exploit protection | Little. Some anti-tamper SDKs debug their own code and fail unless this is allowed. |
| **Dynamic code loading** | Same screen | Little, and it is the most useful toggle on the board — it resolves the "unsecured device" error in several Indian banking apps. |
| **Exploit protection compatibility mode** | Same screen | Real. GrapheneOS's own warning: the app crashed because a memory corruption bug was detected, and that bug may be exploitable by an attacker. |
| **Secure app spawning** (device-wide) | Settings → Security & privacy → Exploit protection | Serious. See below. |

Disabling **secure app spawning** is the one to think about. It reverts app spawning to the traditional Zygote model, so every app process shares the same random secrets — for address-space layout, stack protection, memory tagging, pointer authentication and heap randomisation. It applies across every profile on the device, which means an app running in one profile can observe the values used by an app in another. That is a device-wide reduction in exploit mitigations, taken on to satisfy one app.

Try the per-app toggles first. They are cheap, they are reversible, and they resolve more of these cases than the device-wide one does.

**Clear the app's storage between attempts.** A banking app that has decided your device is unacceptable tends to keep that decision, so a toggle change will look like it did nothing.

## Fixability

| Verdict | Meaning |
|---|---|
| **Nothing to fix** | The app works. |
| **Not fixable** | No workaround exists, and none is plausible. |
| **Fixable with steps** | Works if you change something first. The steps are listed. |
| **Use an alternative** | The app cannot work, but another app, a website, or a piece of hardware can do the same job. |
| **Unknown** | Nobody has tried yet. This is not the same as not fixable. |

The difference between **not fixable** and **unknown** matters more than any other distinction here. `Not fixable` means stop looking. `Unknown` means you might be the person who finds out.

## Alternatives

Saying an app is broken is only half an answer. Every entry with a `not-possible` or `use-an-alternative` verdict also lists what to do instead — a website, a different app, a physical card, a phone call, a branch.

**Each alternative states how much it actually covers.** This is the part that other resources leave out. "Use the website instead" is misleading advice when the website cannot make a payment, so an alternative is marked either **replaces it** or **partial**, and a partial one has to say what is lost.

The worked example is HDFC. Browser net banking restores account access — balances, transfers, statements, card controls. It gives you no UPI, and UPI is the reason most people in India open the app. Recording that as "partial" rather than "works instead" is the difference between useful and misleading.

## How a verdict is derived

Verdicts are computed at build time from the reports. They are never written by hand, because a hand-written verdict drifts away from the reports it claims to summarise.

- **The verdict is the newest report's result.** Not an average. Averaging two conflicting reports produces a value that describes neither of them.
- **Confidence is the number of recent reports that agree.** Shown as "3 reports agree".
- **Dissent is counted, not hidden.** If recent reports disagree with the verdict, that is displayed rather than smoothed away.
- **Last verified is the newest report date**, and it is always shown.

## What a country page shows

A status belongs to an app in a country. It does not belong to the country.

A country page therefore carries counts, not a verdict: how many apps it tracks, how many anyone has reported on, and how many are broken, unavailable or degraded. Working apps get no badge — they are the baseline, and a badge saying so is noise. A country nobody has tested says so, rather than showing a working status by default.

The same applies to a service type. "Payments and UPI: 4 broken of 5" is a fact. "Payments and UPI is broken" would not be, and neither would "Payments and UPI works".

## Where the reports come from

Most entries here rest on the GrapheneOS discussion forum and on the community compatibility tracker maintained by PrivSec.dev, which is the dataset the GrapheneOS project itself points readers to for banking apps. It covers several hundred apps and links each one to a report thread.

Two things are worth knowing when you read an entry that cites it. It is crowd-sourced, and GrapheneOS explicitly makes no guarantee about its validity. And being *listed* is not the same as having been tested recently — the list records apps verified as compatible at some point, and delists them by striking them through. Where a listing and a dated report disagree, this board follows the dated report and records the disagreement rather than resolving it silently.

## Staleness

An entry whose newest report is more than 180 days old is marked as possibly out of date. A monthly job collects them into one issue.

GrapheneOS ships every few days, and app behaviour changes with it. A verdict from a year ago is a historical claim, not a current one. Treat it accordingly.

## Who verified it

| Tier | Meaning |
|---|---|
| **Community report** | One person's report. Not reproduced. This is the default, and it is fine. |
| **Verified by contributor** | Independently reproduced by a trusted contributor. |
| **Verified by maintainer** | Reproduced and confirmed by a maintainer. |
| **Imported, not reproduced** | Taken from a public source rather than tested by anyone here. |

## Imported reports

Some entries were seeded from public forum threads, issue trackers and news reports rather than tested by a contributor to this project. Those reports carry a link to their source and are labelled **Imported, not reproduced**.

**Imported reports have not been reproduced.** They are a lead, not a finding. Contributors are not permitted to submit them — if you have not run the app yourself, it does not belong here.

An imported report may leave the build, device and profile fields empty. That is deliberate. Where the original source did not state a build number, this site leaves the field blank rather than inventing one. A guessed build is worse than an empty field, because it looks like evidence.

Imported reports rank below community reports when working out how much agreement a verdict has.

## Corrections

The first version of this board was assembled from public sources without independent checking, and a later review found several entries were wrong. They have been corrected, and the corrections are recorded here rather than quietly edited away.

| Entry | What it said | What is true |
|---|---|---|
| **Netflix** | Playback permanently capped at Widevine L3, not fixable. | The L3 cap was an October 2023 regression, fixed in release `2023102300`. GrapheneOS supports Widevine L1 on Pixels. |
| **HDFC Bank** | Detects custom firmware, permanently broken. | An OS regression from a third-party security SDK, fixed by GrapheneOS in July 2026. The app works. |
| **Google Wallet** | Tap-to-pay is impossible; use an NFC sticker. | Google Wallet tap-to-pay is impossible. Contactless payment is not — bank apps with their own NFC stack and Curve Pay both work. The sticker advice had no evidence behind it and was removed. |
| **WhatsApp** | Google Drive chat backup does not work. | It works if Play Services and Google Drive are installed and signed in before WhatsApp. Install order is the variable. |
| **PhonePe** | Flags your account as suspicious. | A single unreproduced forum post, contradicted by the community compatibility list. Removed. |
| **Android Auto** | Wired works, only wireless is broken. | An independent month-long review found it unreliable on both. Profile matters: it needs the owner profile. |
| **Bitwarden** | Works fully. | Works, but the official F-Droid build excludes Firebase Messaging, so vault sync is manual. |
| **Google Maps, Instagram** | Cited sources that do not mention these apps. | Reports removed. Both entries now carry no reports rather than a fabricated citation. |

Two lessons were taken from this and written into the contributing guide. First, every claim needs a source that actually supports it. Second, an empty entry is better than a confident wrong one — several of the errors above would have been avoided by leaving the field blank.

## What this site does not claim

- That GrapheneOS is secure, or that any device is.
- That an app listed as working is safe, or respects your privacy. Functional and trustworthy are different questions.
- That a status is current. Check the date on every entry before relying on it.
- That coverage is even. The board is strongest on India and Europe, thin on government identity apps outside India, and has no entries at all for work device-management software.

Nothing here is affiliated with the GrapheneOS project.
