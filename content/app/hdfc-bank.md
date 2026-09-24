---
title: HDFC Bank
slug: hdfc-bank
package: com.hdfcbank.android.now
developer: HDFC Bank
service_type: banking
countries: [IN]
requires_play_services: true
links:
  homepage: https://www.hdfcbank.com
  play_store: https://play.google.com/store/apps/details?id=com.hdfcbank.android.now
  fdroid: null
alternatives:
  - kind: browser
    label: HDFC net banking in a browser
    covers: partial
    detail: "hdfcbank.com gives you account access: balances, statements, NEFT/RTGS/IMPS transfers, bill payments, card controls and limits, cheque book requests, and deposits."
    limitation: "No UPI. A browser cannot scan a payment QR code or send a VPA-to-VPA payment, and you lose the app's push-based transaction approvals. For most Indian users UPI is the main payment rail, so this recovers account access rather than payment ability."
    url: https://www.hdfcbank.com/
  - kind: phone
    label: Phone banking
    covers: partial
    detail: "HDFC's phone banking handles balance enquiries, card blocking, and some transfers through an IVR menu."
    limitation: "Slow, and the menu tree is long. Needs the registered mobile number for the OTP."
    url: null
  - kind: in-person
    label: A branch or ATM
    covers: partial
    detail: "Anything the app will not do can still be done at a branch, and cash withdrawals work at any ATM."
    limitation: "Requires going there, and branch hours."
    url: null
reports:
  - date: 2026-07-27
    build: null
    device: pixel-9
    profile: owner
    country: IN
    play: sandboxed
    result: works-with-setup
    blocked_reason: exploit-protection
    fixability: possible-with-steps
    workaround: "Allow Native code debugging and Dynamic code loading for the HDFC app under Settings → Apps → HDFC Bank App → Exploit protection. Dynamic code loading from storage is the one that matters: with it restricted, the app reports an insecure device regardless of anything else. If it still refuses, check for remote-desktop apps such as AnyDesk or RustDesk, and for anything holding an accessibility service: the app detects those and treats them as tampering."
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/799"
  - date: 2026-07-16
    build: null
    device: null
    profile: null
    country: IN
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://github.com/GrapheneOS/os-issue-tracker/issues/8311"
---

The app works on GrapheneOS once one per-app setting is changed.

The cause is unusual and worth knowing: GrapheneOS's own hardening trips the app's anti-tamper SDK, which reads restricted dynamic code loading as tampering. Nothing about the device is insecure, and relocking the bootloader or reinstalling Play Services changes nothing.

## Pixel 10 is unproven

As of July 2026, nobody had reported HDFC working there, including on a clean device with only Play Services, the Play Store and the app installed.

If a banking app reports an insecure device and Play Integrity is clearly not involved, check exploit protection before concluding the bank has blocked GrapheneOS. Several Indian banking apps share the same anti-tamper SDK, so they fail together when an OS change upsets it.
