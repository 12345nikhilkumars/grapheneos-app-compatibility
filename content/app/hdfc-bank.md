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

The HDFC app works on GrapheneOS, with one per-app setting to check. It was broken for a few days in July 2026, and the cause turned out to be GrapheneOS rather than HDFC.

**This entry previously said the opposite.** It claimed HDFC detected custom firmware and refused to run, that there was no workaround, and that the verdict was `not-possible`. That was wrong, and it is the kind of wrong that costs someone a phone purchase.

It was then wrong in a smaller way: for a while it said `works` with nothing to fix, which was also too generous. The app works, but on some devices it needs an exploit protection setting changed first, and on the Pixel 10 series it has not been made to work at all.

## The thing worth taking away

Most failures on this board are an app deciding the operating system is unacceptable. This one is the opposite, and it is the reason a separate reason code exists for it: **GrapheneOS's own hardening was the problem.**

The app's anti-tamper SDK inspects how the app was loaded, and GrapheneOS's restrictions on dynamic code loading look to it exactly like tampering. Nothing about the device is insecure, and no amount of relocking the bootloader or reinstalling Play Services changes it. One per-app toggle does.

If a banking app reports an insecure device on GrapheneOS and Play Integrity is clearly not involved, check exploit protection before concluding the bank has blocked the platform.

## What actually happened

After the `2026071100` update, the app began intermittently showing an "unsecured device" alert. It was not consistent: closing and reopening the app two or three times cleared it, every time it happened.

The same update broke ICICI and Canara too, which was the clue that this was not a bank policy decision. A GrapheneOS maintainer traced it to the **V-KEY V-OS Mobile App Protection SDK**, which checks Linux mount IDs and breaks when mount namespaces are created after early boot. It was fixed in a follow-up release.

So: an OS regression that a third-party security SDK tripped over, found and fixed within days. Not a bank blocking GrapheneOS.

## If you hit this

Update GrapheneOS. If you are on a build from around `2026071100`, that is the whole fix.

If the app still refuses to run on a current build, check the exploit protection settings before anything else. Under **Settings → Apps → HDFC Bank App → Exploit protection**, allow **Native code debugging** and **Dynamic code loading**. The second one is the one that matters: with dynamic code loading restricted, the app reports an insecure device no matter what else you change, and it reports it in a way that looks like a firmware check.

Two further things are worth knowing, both from the community tracker rather than from GrapheneOS:

- **Another app on the phone can trip it.** The check is an anti-tamper SDK, and it treats remote-desktop tools such as AnyDesk and RustDesk, and anything holding an accessibility service, as evidence of tampering. If the app works for other people on the same build, this is the first thing to look at.
- **The Pixel 10 series is unresolved.** As of July 2026 nobody had reported getting HDFC working on a Pixel 10, including on a clean device with only Play Services, the Play Store and the app itself installed. If you are on a Pixel 10, treat this entry as unproven for your device.

## Technical detail

The V-KEY SDK is used by a number of Indian banking apps, which is why several failed together. It performs its own environment check rather than calling Play Integrity, and the check is sensitive to details of the Linux namespace layout that have nothing to do with whether the device is secure.

Two things follow from that. First, "several banking apps broke at once" is usually an OS-level change rather than a coordinated decision by several banks. Second, a bank app naming custom firmware in its error message does not by itself mean the app can never work; it means a check failed, and checks can be fixed.

## On the browser fallback

The alternatives above are listed in order of how much they actually replace. Net banking in a browser is the practical one, and it is important to be clear about its limit: **it does not give you UPI.** Browser banking covers account access, not the payment rail most people in India use day to day. If UPI is the reason you open the app, the browser is not a substitute.
