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
    label: A bank app with its own UPI
    covers: partial
    detail: "Most Indian banks ship UPI inside their own app, and those have a much better record on GrapheneOS than the standalone payment apps. Axis, ICICI, Kotak and HDFC all work, and HDFC's UPI has been the subject of its own fix. If PhonePe will not behave, this is the closest thing to a direct replacement."
    limitation: "You lose PhonePe's wallet, its offers, and its non-bank features. You also need an account at the bank whose app you use."
    url: null
  - kind: browser
    label: PhonePe's website
    covers: partial
    detail: "PhonePe offers some account and recharge services on the web."
    limitation: "No UPI payments. The web interface does not replace the app's payment function."
    url: https://www.phonepe.com/
reports:
  - date: 2026-09-10
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: works-with-setup
    blocked_reason: play-services-required
    fixability: possible-with-steps
    workaround: "Grant the sandboxed Play Store and Play Services every permission they ask for — Nearby devices is the one that matters — turn on Exploit protection compatibility mode for PhonePe, set its battery usage to unrestricted, and sign in over mobile data rather than Wi-Fi. Registration is the step that fails, so the network you use while registering is part of the setup."
    tier: imported
    source: "https://privsec.dev/posts/android/banking-applications-compatibility-with-grapheneos/"
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
  - date: 2025-09-30
    build: null
    device: null
    profile: owner
    country: IN
    play: sandboxed
    result: works-with-setup
    blocked_reason: play-services-required
    fixability: possible-with-steps
    workaround: "Resolved in the community compatibility tracker by granting the Nearby devices permission to Play Services, enabling compatibility mode, and registering over cellular data instead of Wi-Fi."
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/134"
---

PhonePe works, and getting it to work takes specific setup rather than luck. Two independent sources agree on that, and both describe the same steps.

**This entry has now been wrong in both directions, and the history is worth keeping.** It first said PhonePe flags your *account* as suspicious and warned readers to test with an account they could afford to lose. That claim came from a single forum post, was never reproduced, and was contradicted by the community compatibility list. It was removed. The replacement verdict — `broken` — was then drawn from *the same post*, which is not how this board is supposed to work, and that has now been corrected too.

## What actually happens

The app installs and runs. Registration is where it fails, and it fails for a configuration reason rather than an attestation one. The community tracker closed its PhonePe report with a working resolution: grant Play Services the **Nearby devices** permission, turn on **Exploit protection compatibility mode** for PhonePe, give it unrestricted battery usage, and register over **mobile data rather than Wi-Fi**. Several people in the India thread independently reported the same thing, and at least one has been using it on GrapheneOS for years.

None of those steps is about convincing PhonePe that the OS is stock. There is no evidence it checks. The failure behaves like a permissions or connectivity problem in the setup flow.

## Why the verdict still shows a disagreement

One report from June 2026 says PhonePe stopped working for payments. It is a single unverified post with no logs and no app version, and it is the same post that produced the account-flag claim we removed. It is kept in the data rather than deleted, so the page shows the conflict instead of hiding it.

If you are setting up PhonePe now, the setup above is the thing to try. If it fails for you, that June report is the reason the board will not promise it works.

## Technical detail

UPI apps sit on top of a bank-to-bank network with its own device binding rules, so a failure in the payment flow can originate in the app, in the NPCI layer, or in the issuing bank's checks. That is why the reason on the June report is recorded as `unknown` — nobody established it, and guessing would send the next person down a path that cannot work.

For contrast, the failures that *are* clearly attestation-driven in India look different: Paytm names the problem and refuses to continue. PhonePe's setup problems do not.
