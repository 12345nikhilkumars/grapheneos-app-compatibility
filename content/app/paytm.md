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
    label: Keep UPI on a second device
    covers: full
    detail: "If UPI matters to you, the dependable answer is a second phone running stock Android. Nothing on GrapheneOS currently substitutes for the UPI rail."
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
---

Paytm refuses to run and tells you the device is running custom firmware. Unlike the entries where the cause is a mystery, this one names its reason.

That is useful information: a named custom-firmware check is a deliberate block rather than a security library misfiring, and it tells you the app is inspecting the operating system directly.

**One caution.** This comes from a single forum post. An earlier report a year before describes Paytm working, and the community compatibility list has it working too. It may have regressed, or the block may be partial. Treat the verdict as the most recent report rather than as settled.

## Technical detail

A custom-firmware message means the app is inspecting the device directly rather than relying on Play Integrity or SafetyNet. Locking the bootloader does not satisfy this kind of check, and neither does installing sandboxed Play Services — the app is not asking about Play, it is asking about the operating system.

`fixability` is `unknown` rather than `not-possible` only because nobody has documented an attempt to work around it. Given that the check is deliberate and enforced in the app, expect `not-possible` to be the eventual verdict.

If you need UPI and you are choosing apps, the ones that fail with a named firmware check are the least likely to be fixable. The ones that fail silently, like PhonePe, are at least worth retesting after an update.
