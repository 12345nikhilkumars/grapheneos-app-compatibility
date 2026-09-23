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
alternatives:
  - kind: other
    label: Keep UPI on a second device
    covers: full
    detail: "If UPI matters to you, the dependable answer is a second phone running stock Android, or keeping UPI on the phone you are replacing. Nothing on GrapheneOS currently substitutes for the UPI rail."
    url: null
  - kind: hardware
    label: Card, cash, or UPI on someone else's phone
    covers: partial
    detail: "Card terminals and cash work anywhere they work. For merchant QR codes, asking to pay by card or cash is often the only option."
    limitation: "Most small Indian merchants are UPI-only or prefer it, and person-to-person transfers have no card equivalent at all."
    url: null
reports:
  - date: 2026-06-29
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: unknown
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://discuss.grapheneos.org/d/37215-nearly-all-indian-upi-apps-have-blocked-payments-on-grapheneos"
---

UPI payments through Google Pay stopped working for GrapheneOS users. The app runs and the rest of it behaves normally, but the payment flow does not complete.

This is part of a wider pattern: the Indian UPI apps tracked on this board — Google Pay, PhonePe, Paytm, BHIM — all fail, and they fail in different ways. That suggests the restriction is not one app's decision but something in the UPI stack or in how these apps verify a device.

**Do not plan around UPI working on GrapheneOS until you have tested it yourself on a current build.** This is the single most consequential thing to check before switching in India.

## Technical detail

No cause has been confirmed. UPI apps sit on top of a bank-to-bank network with its own device binding rules, and a failure could originate in the app, in the NPCI layer, or in the issuing bank's own checks. Until someone traces it, the honest answer is that it is unknown.

The `fixability` value is `unknown` rather than `not-possible` for the same reason: nobody has established whether a workaround exists, which is not the same as proving one does not.

## On the sources

The reports behind the Indian payment entries come from a small number of forum posts, and this one is not strong evidence. It is a single thread. It is included because two separate threads a year apart agree that Google Pay used to work and then stopped, and because the community-maintained compatibility list omits Google Pay entirely — but a report from someone on a current build would be far more useful than this entry.

If you are in India and you use UPI, your report is worth more here than anywhere else on the board.
