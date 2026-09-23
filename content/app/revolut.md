---
title: Revolut
slug: revolut
package: com.revolut.revolut
developer: Revolut
service_type: banking
countries: [GB, FR, DE, NL, ES, IT, SE, AT, CH]
requires_play_services: true
links:
  homepage: https://www.revolut.com
  play_store: https://play.google.com/store/apps/details?id=com.revolut.revolut
  fdroid: null
alternatives:
  - kind: in-person
    label: A bank that does not check the device
    covers: full
    detail: "Plenty of banks do not inspect the operating system at all. The community-maintained compatibility list tracks which banks work, country by country, and it is the fastest way to find one for yours."
    url: https://privsec.dev/posts/android/banking-applications-compatibility-with-grapheneos/
  - kind: browser
    label: Revolut's web app
    covers: partial
    detail: "web.revolut.com gives balances, statements, transfers, card controls and top-ups."
    limitation: "It does not help if your account has already been flagged. Revolut's block is applied to the account rather than only to the device, so the website may be restricted too. If that has happened, the only route is Revolut support."
    url: https://www.revolut.com/
reports:
  - date: 2026-08-06
    build: null
    device: null
    profile: null
    country: GB
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: not-possible
    workaround: null
    tier: imported
    source: "https://cybernews.com/privacy/grapheneos-says-revolut-is-blocking-users-again-and-this-time-its-personal/"
---

Revolut does not work on GrapheneOS, and unlike most entries on this board it is not an accident. The company is reported to detect GrapheneOS specifically and to block the account rather than only the app.

This is the most serious banking problem documented for GrapheneOS, because the failure is not confined to the phone. Affected users report being told to factory-reset to a stock OS, and some report losing access to their account rather than just to the app.

**If you bank with Revolut and are considering GrapheneOS, read this before you switch.**

## The timeline

- **Late 2024.** Reports begin of Revolut refusing to run on custom firmware. The community works on workarounds; some succeed for a while.
- **Through 2025.** The block becomes less consistent, then returns.
- **August 2026.** The GrapheneOS project publicly accuses Revolut of deliberately targeting its users again, with new detection methods. This is where the current verdict comes from.

The pattern — detection, workaround, new detection — is why this entry is recorded as `not-possible`. It is not that nobody has found a way around it. It is that the workarounds keep being closed, and each cycle risks the account rather than the app.

## Technical detail

Revolut performs its own environment checks rather than relying only on Play Integrity. Reports describe the check running during sign-in, with the app refusing to proceed once it decides the device is not stock. Locking the bootloader does not change the outcome, and neither does installing sandboxed Play Services — the app is asking about the operating system.

Because the response is applied at account level, the usual advice about workarounds does not apply. Retrying, reinstalling, or clearing data is more likely to look like suspicious activity than to help.

## What to do instead

Keep Revolut on a stock device if you need it, and use a different bank for the GrapheneOS phone. The compatibility list linked above is organised by country and is the practical way to find one — many banks in the same countries have no device check at all, and the difference between them is not something you can predict from the brand.

## A note on scope

This entry exists because it was missing. The board previously covered banking problems in India in detail while omitting the best-documented banking failure in Europe, which was a real gap rather than a judgement about which countries matter.
