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

UPI payments through Google Pay have been reported as broken, and the evidence is genuinely mixed rather than merely thin.

**The framing this entry used to carry is now out of date, and it was too bleak.** It said the Indian UPI apps "all fail". They do not. PhonePe works with a specific setup, HDFC's app works with one exploit protection setting changed, and Curve handles contactless. What fails is narrower than that: Paytm and BHIM are the two that are actually blocked. Treating the whole rail as dead overstated the problem in the direction that costs someone a phone.

## What is actually reported

Two threads disagree, and the disagreement is informative:

- One report says Google Pay stopped working for payments, with the app itself behaving normally otherwise.
- The longer India thread reports it working for some people and not others, with NFC payments failing, one user stuck at the SMS step during setup, and a workaround: **enable Dynamic code loading from storage** for the app under `Settings → Apps → Google Pay → Exploit protection`. That is the same setting that resolves HDFC's "unsecured device" error, which makes it the first thing worth trying here.

If you are setting Google Pay up, change that setting before concluding anything.

## Technical detail

No cause has been confirmed. UPI apps sit on top of a bank-to-bank network with its own device binding rules, and a failure could originate in the app, in the NPCI layer, or in the issuing bank's own checks. Until someone traces it, the honest answer is that it is unknown.

The `fixability` value is `unknown` rather than `not-possible` for the same reason: nobody has established whether a workaround exists, which is not the same as proving one does not.

## On the sources

This is the weakest-sourced entry on the board and it should be treated that way. Its verdict rests on a single forum post in which Google Pay is mentioned in passing alongside four other apps — no app version, no build, no logs. A claim from that same post about PhonePe has since been withdrawn.

The community-maintained compatibility list, which covers several hundred banking apps, does not list Google Pay at all. That is not evidence either way; it means nobody has filed a report there.

If you are in India and you use UPI, your report is worth more here than anywhere else on the board — and this entry is the one that most needs it.
