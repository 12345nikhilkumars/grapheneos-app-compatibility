---
title: Google Pay (India)
slug: google-pay-india
package: com.google.android.apps.nbu.paisa.user
developer: Google
service_type: payments
countries: [IN]
requires_play_services: true
links:
  homepage: https://pay.google.com
  play_store: https://play.google.com/store/apps/details?id=com.google.android.apps.nbu.paisa.user
  fdroid: null
reports:
  - date: 2026-09-10
    build: "2026091000"
    device: pixel-8
    profile: owner
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: unknown
    fixability: unknown
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/37215-indian-upi-apps"
---

UPI payments through Google Pay stopped working for GrapheneOS users. The app runs and the rest of it behaves normally, but the payment flow does not complete.

**Treat this entry with more caution than the others.** The reports are consistent that it broke, but they are not consistent about why, and this is the area where third-party guides disagree most sharply. Some sources claim every major UPI app works fine; those sources are machine-generated and contradict the people actually using the phones.

Do not plan around UPI working on GrapheneOS until you have tested it yourself on a current build.

## Technical detail

No cause has been confirmed. UPI apps sit on top of a bank-to-bank network with its own device binding rules, and the failure could originate in the app, in the NPCI layer, or in the issuing bank's own checks. Until someone traces it, the honest answer is that it is unknown.

The `fixability` value is `unknown` rather than `not-possible` for the same reason: nobody has established whether a workaround exists, which is not the same as proving one does not.
