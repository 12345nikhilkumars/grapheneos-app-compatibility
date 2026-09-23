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

The HDFC app works on GrapheneOS. It was broken for a few days in July 2026, and the cause turned out to be GrapheneOS rather than HDFC.

**This entry previously said the opposite.** It claimed HDFC detected custom firmware and refused to run, that there was no workaround, and that the verdict was `not-possible`. That was wrong, and it is the kind of wrong that costs someone a phone purchase.

## What actually happened

After the `2026071100` update, the app began intermittently showing an "unsecured device" alert. It was not consistent — closing and reopening the app two or three times cleared it, every time it happened.

The same update broke ICICI and Canara too, which was the clue that this was not a bank policy decision. A GrapheneOS maintainer traced it to the **V-KEY V-OS Mobile App Protection SDK**, which checks Linux mount IDs and breaks when mount namespaces are created after early boot. It was fixed in a follow-up release.

So: an OS regression that a third-party security SDK tripped over, found and fixed within days. Not a bank blocking GrapheneOS.

## If you hit this

Update GrapheneOS. If you are on a build from around `2026071100`, that is the whole fix.

If the app refuses to run on a current build, that is a new and different problem, and it is worth a report — see the contribute section below.

## Technical detail

The V-KEY SDK is used by a number of Indian banking apps, which is why several failed together. It performs its own environment check rather than calling Play Integrity, and the check is sensitive to details of the Linux namespace layout that have nothing to do with whether the device is secure.

Two things follow from that. First, "several banking apps broke at once" is usually an OS-level change rather than a coordinated decision by several banks. Second, a bank app naming custom firmware in its error message does not by itself mean the app can never work — it means a check failed, and checks can be fixed.

## On the browser fallback

The alternatives above are listed in order of how much they actually replace. Net banking in a browser is the practical one, and it is important to be clear about its limit: **it does not give you UPI.** Browser banking covers account access, not the payment rail most people in India use day to day. If UPI is the reason you open the app, the browser is not a substitute.
