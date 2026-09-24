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

BHIM does not work, and the reason is on the record rather than inferred: BHIM support told a user that registration could not be completed because the device **"does not meet the security standards mandated by the Reserve Bank of India"**, and advised using another device.

## Two different checks

**"Rooting detected"** is the app inspecting the device itself, and relocking the bootloader does not satisfy it. The onboarding failure that follows looks like server-side enforcement, which fits the RBI reply: the decision is not made on the phone.

Because the requirement is regulatory rather than one bank's risk appetite, no local change is likely to settle this permanently. It has flipped before, though: working through 2023 and 2024, broken in June 2025, working again in October 2025 by installing Play Services, giving it SMS but not network access, logging in, then uninstalling it. Worth watching rather than treating as final.

## Before you install it

Tracker contributors have documented extensive behavioural analytics on spending, added around version 3.8.7, with no opt-out. Separate from whether it runs, but it belongs here.
