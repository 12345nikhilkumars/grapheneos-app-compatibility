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
reports:
  - date: 2026-09-10
    build: "2026091000"
    device: pixel-8
    profile: owner
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: unknown
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/37215-indian-upi-apps"
---

Paytm refuses to run and tells you the device is running custom firmware. Unlike the entries where the cause is a mystery, this one names its reason.

That is useful information: a named custom-firmware check is a deliberate block, not a security library misfiring.

## Technical detail

A custom-firmware message means the app is inspecting the device directly rather than relying on Play Integrity or SafetyNet. Locking the bootloader does not satisfy this kind of check, and neither does installing sandboxed Play Services — the app is not asking about Play, it is asking about the operating system.

`fixability` is `unknown` rather than `not-possible` only because nobody has documented an attempt to work around it. Given that the check is deliberate and enforced in the app, expect `not-possible` to be the eventual verdict.

If you need UPI and you are choosing apps, the ones that fail with a named firmware check are the least likely to be fixable.
