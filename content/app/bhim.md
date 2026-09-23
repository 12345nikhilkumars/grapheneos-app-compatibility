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

BHIM is the NPCI's own UPI app, which makes its behaviour the most informative of the Indian payment entries. It reports that the device is running custom firmware and refuses to continue.

Because NPCI operates the UPI network itself, a block here carries more weight than a block in a third-party app. It suggests the restriction sits at the network level rather than being one bank's decision.

**Reports conflict, however.** Earlier threads describe some users getting BHIM working, while later ones describe the custom-firmware rejection. The dates matter, and the entry reflects the most recent report.

## Technical detail

If the block originates at NPCI rather than in the app, no local change will resolve it, because the device check would be part of the payment network's own rules.

The conflicting reports are recorded rather than resolved. The current verdict is `broken` because that is the newest report, and the dissent is visible in the report history below rather than being averaged away. Anyone who gets BHIM working on a current build should submit a report — it would change the verdict.
