---
title: PhonePe
slug: phonepe
package: com.phonepe.app
developer: PhonePe
service_type: payments
countries: [IN]
requires_play_services: true
links:
  homepage: https://www.phonepe.com
  play_store: https://play.google.com/store/apps/details?id=com.phonepe.app
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

PhonePe does not simply refuse to open. It flags the account as suspicious, which is a worse failure than a hard block — the app appears to work, and the problem surfaces when you try to pay.

That behaviour makes this one harder to diagnose than a straightforward rejection, and it means the risk is not limited to the payment itself.

## Technical detail

The reported symptom is an account-level flag rather than a device-level rejection, which points at a server-side risk decision rather than a local integrity check. If that is what is happening, reinstalling or changing settings will not help — the flag is attached to the account.

Two things follow from that. First, do not keep retrying: repeated suspicious-looking attempts are exactly what triggers risk systems. Second, if your PhonePe account matters to you, test with an account you can afford to lose, or use a different UPI app for the experiment.

The cause is recorded as `unknown` because no one has confirmed it. The account-flag detail comes from a single forum thread and has not been reproduced.
