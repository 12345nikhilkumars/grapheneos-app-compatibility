---
title: Google Wallet
slug: google-wallet
package: com.google.android.apps.walletnfcrel
developer: Google
service_type: payments
global: true
requires_play_services: true
links:
  homepage: https://wallet.google
  play_store: https://play.google.com/store/apps/details?id=com.google.android.apps.walletnfcrel
  fdroid: null
alternatives:
  - kind: app
    label: A bank app with its own NFC stack
    covers: full
    detail: "Some banks handle contactless payment inside their own app instead of routing it through Google Wallet. Crédit Mutuel and CIC in France do this, and it works with no Play Services installed at all."
    url: null
  - kind: app
    label: Curve Pay
    covers: partial
    detail: "Curve issues a virtual card and performs contactless payment itself through host card emulation. Once it is activated, set it as the default wallet under Settings, Connected devices, Connection preferences, NFC, Contactless payments."
    limitation: "Curve's activation step was broken for about nine months and was fixed in version 5.42.0 in June 2026, so update the app before concluding it does not work. Curve also does not support American Express cards. Its own entry covers the detail."
    url: https://www.curve.com/
  - kind: hardware
    label: A watch, or a physical card
    covers: full
    detail: "Wear OS and Garmin watches perform their own attestation independently of the phone, so tap-to-pay works from the wrist even when it fails on the phone."
    url: null
reports:
  - date: 2026-07-09
    build: null
    device: pixel-10-pro-xl
    profile: null
    country: FR
    play: sandboxed
    result: broken
    blocked_reason: play-integrity
    fixability: possible-via-workaround
    workaround: "Use a bank app with its own NFC stack, Curve Pay, or a watch. Google Wallet itself cannot be made to work — the check is enforced on Google's side."
    tier: imported
    source: "https://discuss.grapheneos.org/d/38083-nfc"
---

The Wallet app installs and runs normally. You can add cards, and stored passes, tickets and loyalty cards all display correctly.

What does not work is **tap-to-pay**. Holding the phone to a terminal fails with a message saying the device does not meet contactless payment security requirements. No setting changes this.

This is the most commonly reported thing that simply does not work on GrapheneOS, and it is worth knowing before you switch rather than after.

**The important correction to make here:** tap-to-pay being broken in Google Wallet does not mean contactless payment is impossible on GrapheneOS. It means *Google's* wallet is unavailable. Several other routes work, and they are listed above. Earlier versions of this entry said a workaround was to buy an NFC payment sticker; nobody has reported doing that, and it should not have been here.

## Technical detail

Tap-to-pay requires the app to pass a Play Integrity check that the device is running an unmodified, Google-approved operating system. GrapheneOS cannot pass it, and the decision is made on Google's servers rather than inside the app, so there is nothing to patch locally. Locking the bootloader does not help — the check fails either way.

Card storage and pass display do not require the check, which is why they keep working.

The alternatives work for a different reason in each case. A bank app with its own NFC stack never asks Google anything, so it is unaffected. Curve performs host card emulation itself and is not gated on attestation at all — its setup step was broken for most of a year and was fixed in June 2026, which is a reminder that "does not work" and "does not work yet" look identical from the outside. A watch attests on its own hardware, so the phone's verdict is irrelevant.

If you rely on tap-to-pay, the thing to check before switching is whether your own bank has a native NFC option. That is a question for the bank, not for GrapheneOS.
