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
reports:
  - date: 2026-08-20
    build: "2026081300"
    device: pixel-8
    profile: owner
    country: US
    play: sandboxed
    result: broken
    blocked_reason: hardware-attestation
    fixability: possible-via-workaround
    workaround: "Use a Wear OS or Garmin watch for tap-to-pay, or an NFC payment sticker such as Curve or Tapster."
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://github.com/GrapheneOS/os-issue-tracker/issues/1506"
---

The Wallet app installs and runs normally. You can add cards, and stored passes, tickets and loyalty cards all display correctly.

What does not work is **tap-to-pay**. Holding the phone to a payment terminal fails, with a message saying the device does not meet security requirements. There is no setting that changes this.

This is the single most commonly reported thing that simply does not work on GrapheneOS, and it is worth knowing before you switch rather than after.

## Technical detail

Tap-to-pay requires a hardware-backed attestation that the device is running an unmodified, Google-approved operating system. GrapheneOS cannot produce that attestation, and the check is enforced on Google's side rather than in the app, so there is nothing to patch locally. Locking the bootloader does not help — the attestation fails regardless.

Card storage and pass display do not require attestation, which is why they continue to work.

A watch is the usual workaround because Wear OS devices perform their own attestation, independent of the phone.
