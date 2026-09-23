---
title: Curve
slug: curve
package: com.imaginecurve.curve.prd
developer: Curve
service_type: payments
countries: [GB, DE, FR, NL, AT, SE, ES, IT]
requires_play_services: true
links:
  homepage: https://www.curve.com
  play_store: https://play.google.com/store/apps/details?id=com.imaginecurve.curve.prd
  fdroid: null
alternatives:
  - kind: app
    label: Your bank's own contactless app
    covers: partial
    detail: "Several banks ship their own NFC stack and can make contactless payments without Google Wallet. Barclays, Chase and a number of European banks do this, and it works on GrapheneOS."
    limitation: "Only for cards from that bank. You lose Curve's aggregation, its rewards, and the ability to move a payment onto a different underlying card after the fact."
    url: null
  - kind: hardware
    label: A physical contactless card
    covers: full
    detail: "A contactless card does everything Curve Pay does at a terminal, and it needs no setup, no Play Services and no app."
    limitation: "You carry a card. You also lose the aggregation and the cashback."
    url: null
reports:
  - date: 2026-06-06
    build: null
    device: null
    profile: owner
    country: GB
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/679"
  - date: 2026-05-23
    build: null
    device: null
    profile: null
    country: GB
    play: sandboxed
    result: broken
    blocked_reason: unknown
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/679"
  - date: 2025-09-16
    build: null
    device: null
    profile: null
    country: GB
    play: sandboxed
    result: works-degraded
    blocked_reason: unknown
    fixability: unknown
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/679"
---

Curve works on GrapheneOS, including contactless payments, and it is the most practical way to get tap-to-pay back on a phone without Google Wallet.

The app itself has never been the problem. The interesting part is that Curve's contactless feature was broken for about nine months and then fixed, which is worth knowing if you find it failing.

## The timeline

- **September 2025.** The app works, but setting up Curve Pay contactless fails.
- **May 2026.** Still failing on version 5.40.0. One user gets as far as selecting Curve Pay as the payment app in NFC settings but never confirms a terminal transaction.
- **June 2026.** Version 5.42.0 works on GrapheneOS `2026060101`, on a Pixel 10, including NFC payments, installed from the Play Store.

That is the whole story: a feature that was broken, was reported repeatedly, and was fixed. If Curve Pay will not set up for you, update the app before trying anything else.

## Why it matters here

Google Wallet's tap-to-pay does not work on GrapheneOS and is not going to. Curve is the alternative that people actually use, because it does not check whether the operating system is certified — it never used Play Integrity to gate itself.

One limitation worth stating plainly: **Curve does not support American Express cards.** If your card is Amex, Curve is not an option for it.

## Technical detail

Curve sits between the terminal and your underlying cards, so a payment goes through Curve rather than directly to your bank. That has a practical consequence on GrapheneOS: it does not depend on your bank supporting contactless in its own app, which several do not.

The reports that make up this entry come from the community compatibility tracker, which is also where the fixes were confirmed. Where a report is undated in detail — the September 2025 and May 2026 failures do not name a GrapheneOS build — the field is left empty rather than guessed at.
