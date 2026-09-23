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
alternatives:
  - kind: other
    label: Keep UPI on a second device
    covers: full
    detail: "If UPI matters to you, the dependable answer is a second phone running stock Android. Nothing on GrapheneOS currently substitutes for the UPI rail."
    url: null
  - kind: browser
    label: PhonePe's website
    covers: partial
    detail: "PhonePe offers some account and recharge services on the web."
    limitation: "No UPI payments. The web interface does not replace the app's payment function."
    url: https://www.phonepe.com/
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

PhonePe does not work for UPI payments on GrapheneOS, based on the most recent report. The app runs, and the failure shows up when you try to pay.

**This entry previously said something much more alarming, and it should not have.** It claimed PhonePe flags your *account* as suspicious, and warned readers to test with an account they could afford to lose. That claim came from a single forum post, was never reproduced, and is contradicted by the community-maintained compatibility list, which lists PhonePe as working with no negative notes. Presenting it as established was wrong. It has been removed.

If PhonePe is your main UPI app and you switch, test with a small transaction first — that is sensible with any payment app on any OS. But there is no evidence that GrapheneOS puts your PhonePe account at risk.

## Technical detail

The cause is recorded as `unknown` because no one has established it. UPI apps sit on top of a bank-to-bank network with its own device binding rules, and the failure could originate in the app, in the NPCI layer, or in the issuing bank's checks.

Worth noting for contrast: an older report from September 2025 describes PhonePe working after enabling compatibility mode and granting the Nearby devices permission. That report may be obsolete, or it may mean the block is not uniform. Both are recorded rather than one being averaged into the other.

## What would settle it

A report from someone in India on a current build, saying what happened and what the app said when it failed. Two reports a year apart disagree, and the newest one is thin.
