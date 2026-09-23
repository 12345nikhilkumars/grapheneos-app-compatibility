---
title: BHIM
slug: bhim
package: in.org.npci.upiapp
developer: National Payments Corporation of India
service_type: payments
countries: [IN]
requires_play_services: true
links:
  homepage: https://www.npci.org.in
  play_store: https://play.google.com/store/apps/details?id=in.org.npci.upiapp
  fdroid: null
alternatives:
  - kind: other
    label: Keep UPI on a second device
    covers: full
    detail: "If UPI matters to you, the dependable answer is a second phone running stock Android. Nothing on GrapheneOS currently substitutes for the UPI rail."
    url: null
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

BHIM is the NPCI's own UPI app, which makes its behaviour the most informative of the Indian payment entries. It reports that the device is running custom firmware and refuses to continue.

Because NPCI operates the UPI network itself, a block here carries more weight than a block in a third-party app. It suggests the restriction sits at the network level rather than being one company's decision.

**Reports conflict, however.** Earlier threads describe users getting BHIM working, while later ones describe the custom-firmware rejection. The dates matter, and the entry reflects the most recent report rather than a settled answer.

## Technical detail

If the block originates at NPCI rather than in the app, no local change will resolve it, because the device check would be part of the payment network's own rules.

The conflicting reports are recorded rather than resolved. The current verdict is `broken` because that is the newest report, and the dissent is visible in the report history rather than being averaged away. Anyone who gets BHIM working on a current build should submit a report — it would change the verdict.

## Why this matters more than the others

The other Indian payment entries tell you what one app does. This one is the closest thing to a signal about the rail underneath all of them. If NPCI is enforcing a device check, then the UPI apps will keep failing in different ways as each one implements its own version of the same requirement — which is roughly what the reports show.
