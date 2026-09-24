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
    detail: "A second phone running stock Android, or the phone you are replacing, still works as a UPI backup."
    url: null
  - kind: hardware
    label: Card, cash, or UPI on someone else's phone
    covers: partial
    detail: "Card terminals and cash work anywhere they work. For merchant QR codes, asking to pay by card or cash is often the only option."
    limitation: "Most small Indian merchants are UPI-only or prefer it, and person-to-person transfers have no card equivalent at all."
    url: null
reports:
  - date: 2026-09-24
    build: null
    device: pixel-10a
    profile: owner
    country: IN
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: maintainer
    reporter: "@12345nikhilkumars"
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

UPI works through Google Pay on GrapheneOS. Installed into the owner profile with sandboxed Play Services, it needed no per-app setting changed.

**NFC tap-to-pay is untested.** The report covers UPI only.

## If it does not work for you

Enable **Dynamic code loading from storage** for Google Pay under `Settings → Apps → Google Pay → Exploit protection`. That is the setting that resolves HDFC's "unsecured device" error, and the community thread reports it working here too.

## Why a disagreement shows

The dissenting report is a single forum post that mentions Google Pay in passing alongside four other apps, with no app version, build or logs. It is kept rather than deleted so the conflict stays visible.
