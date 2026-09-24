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
  - kind: app
    label: PhonePe
    covers: partial
    detail: "PhonePe works on GrapheneOS with a specific setup, and it is a standalone UPI app rather than a bank's own. It is the closest working equivalent to BHIM."
    limitation: "Different app, different operator, and its own setup requirements. It also fails for some people, and its entry records the conflict rather than resolving it."
    url: https://www.phonepe.com/
  - kind: other
    label: A bank app with its own UPI
    covers: partial
    detail: "Axis, ICICI, Kotak and HDFC all ship UPI inside their own apps and have a better record on GrapheneOS than the standalone payment apps."
    limitation: "You need an account at the bank whose app you use. Some banks restrict UPI registration to one device."
    url: null
reports:
  - date: 2026-09-02
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: play-integrity
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/135"
  - date: 2026-07-27
    build: null
    device: pixel-6a
    profile: owner
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: play-integrity
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/135"
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
  - date: 2025-10-01
    build: null
    device: null
    profile: owner
    country: IN
    play: sandboxed
    result: works-with-setup
    blocked_reason: play-services-required
    fixability: possible-with-steps
    workaround: "Install Play Services, give it SMS permission but not network access, complete BHIM's login, then uninstall Play Services again. Several people reported daily use working afterwards with no Play Services installed at all."
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/135"
---

BHIM does not work. It is the NPCI's own UPI app, so its behaviour says more about the UPI rail than the behaviour of any third-party app does.

**This entry has been corrected twice, and both corrections were in the same direction: from speculation towards evidence.** It used to infer from BHIM's failures that the restriction "sits at the network level". It turns out that is closer to right than the reasoning deserved, because there is now an on-the-record statement: BHIM's own support team told a user that registration could not be completed because the device **"does not meet the security standards mandated by the Reserve Bank of India"**, and advised using a different device.

That is a named policy from a named regulator, not a guess about an app's behaviour. It is the strongest kind of evidence this board can carry.

## The pattern

BHIM has worked on GrapheneOS and stopped, more than once. The oscillation is the point.

- **Through 2023 and 2024.** Works, including with no Play Services at all, though QR scanning needed Play Services to download its detection patterns.
- **June 2025.** Breaks. A community member traces it to version 4.0.2 enforcing the Play Integrity API. BHIM support replies with the RBI standards line above.
- **October 2025.** Works again. The route back in: install Play Services, give it SMS but not network, log in, then uninstall Play Services. The community tracker removes its "not compatible" label.
- **October 2025, later.** Version `253000082` starts refusing to run with developer options enabled, which is a build-property check, and one that forces a reboot to work around.
- **March 2026.** Onboarding fails on a fresh install on a Pixel 7 with "We are unable to onboard you at this time". The reporter notes it is also checking Play Integrity.
- **September 2026.** Confirmed broken.

## What the failures actually are

Two different checks are in play, and telling them apart matters.

The **"rooting detected"** message is the app inspecting the device itself. It is not Play Integrity, and it is not satisfied by relocking the bootloader. It fires before the app gets far enough to fail on anything else.

The **onboarding failure**, the one that says "we are unable to onboard you at this time", happens after that check is satisfied, and looks like server-side enforcement. That is consistent with the RBI standards reply: the decision is not being made on the phone.

## Technical detail

Because the requirement is regulatory rather than a bank's own risk appetite, no local change is likely to settle this permanently. That is a stronger claim than the earlier version of this entry could make, and it is now supported by a vendor statement rather than inference.

The workarounds that have worked historically are worth knowing even though none is currently reported working: the Play Services install-then-uninstall trick from October 2025, and turning developer options off for the `253000082` build. If BHIM matters to you, the report history above is the thing to watch: it has flipped before, and each flip is dated.

## A note on the app itself

BHIM is worth using on privacy grounds only if you have not looked at what it does. Contributors to the community tracker have documented extensive behavioural analytics on spending, added from around version 3.8.7, with no way to opt out. That is a separate question from whether it runs, and it is not one this board is set up to score, but it belongs next to the recommendation, not buried.
