---
title: Paytm
slug: paytm
package: net.one97.paytm
developer: One97 Communications
service_type: payments
countries: [IN]
requires_play_services: true
links:
  homepage: https://paytm.com
  play_store: https://play.google.com/store/apps/details?id=net.one97.paytm
  fdroid: null
alternatives:
  - kind: other
    label: A bank app with its own UPI
    covers: partial
    detail: "Most Indian banks ship UPI inside their own app, and those have a better record on GrapheneOS than the standalone payment apps. Axis, ICICI, Kotak and HDFC all work."
    limitation: "You lose Paytm's wallet, bill payments and ticketing. You also need an account at the bank whose app you use."
    url: null
  - kind: browser
    label: Paytm's website
    covers: partial
    detail: "Paytm offers recharges, bill payments and some ticketing on the web."
    limitation: "No UPI payments, and no QR scanning. The web interface does not replace the app's payment function."
    url: https://paytm.com/
reports:
  - date: 2026-06-29
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://discuss.grapheneos.org/d/37215-nearly-all-indian-upi-apps-have-blocked-payments-on-grapheneos"
  - date: 2026-05-19
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/140"
  - date: 2026-03-09
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/140"
  - date: 2026-02-21
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://discuss.grapheneos.org/d/26888-india-what-upi-apps-still-work-which-bank-apps-still-work"
---

Paytm refuses to run and tells you the device is running custom firmware. It has done this repeatedly through 2026, and the block is deliberate rather than a security library misfiring.

**A caution that matters here.** The community-maintained compatibility list still carries Paytm as compatible, and there is no note attached to it. That list is not wrong often, but it is a summary rather than a fresh test, and it has not kept pace with this app. Two reports from 2026 describe Paytm blocking GrapheneOS outright, and the most recent report on this board agrees. The conflict is recorded rather than resolved: read the provenance line before trusting the verdict above it.

## The pattern

Paytm has oscillated, which is worse than being consistently broken: it means a working report is not evidence that it will keep working.

- **February 2026.** A report on the India thread: "Paytm formally blocks GrapheneOS now. Shows device modification or root detected right after play integrity notif."
- **March 2026.** Version 10.75.6 is reported working.
- **May 2026.** Reported not working again, with screenshots.
- **June 2026.** Reported as still showing a custom-firmware message.

A named firmware check is a deliberate block rather than a bug, and the app naming it is useful information: it tells you Paytm is inspecting the operating system directly.

## Technical detail

A custom-firmware message means the app inspects the device rather than relying only on Play Integrity. Locking the bootloader does not satisfy this kind of check, and neither does installing sandboxed Play Services. The app is not asking about Play, it is asking about the operating system. The February report describes the firmware check firing *after* a Play Integrity notification, so both mechanisms are in play.

`fixability` is `unknown` rather than `not-possible` only because nobody has documented a serious attempt to work around it. Given that the check is deliberate and enforced in the app, expect `not-possible` to be the eventual verdict.

If you need UPI and you are choosing apps, note that the ones failing with a named firmware check are the least likely to be fixable. PhonePe, which fails in its setup flow rather than at a firmware check, is the better bet.
