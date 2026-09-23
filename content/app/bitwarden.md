---
title: Bitwarden
slug: bitwarden
package: com.x8bit.bitwarden
developer: Bitwarden
service_type: security
global: true
requires_play_services: false
links:
  homepage: https://bitwarden.com
  play_store: https://play.google.com/store/apps/details?id=com.x8bit.bitwarden
  fdroid: https://f-droid.org/packages/com.x8bit.bitwarden/
alternatives:
  - kind: app
    label: The Play Store build, if you want push sync
    covers: full
    detail: "The same app from the Play Store includes Firebase Messaging, so vault changes arrive as a notification instead of waiting for the next manual sync."
    url: https://play.google.com/store/apps/details?id=com.x8bit.bitwarden
reports:
  - date: 2026-09-10
    build: null
    device: pixel-8
    profile: owner
    country: US
    play: none
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://github.com/bitwarden/f-droid"
---

Bitwarden works fully, and it is one of the apps that runs best on GrapheneOS because it does not need Play Services at all.

Autofill, biometric unlock, sync, and browser extension pairing all behave normally. It is available on F-Droid as well as the Play Store, so you can install it without sandboxed Play Services if you prefer.

This entry is included as a counterweight to the broken ones. Most apps work, and password managers are a category where the privacy-focused options are actively better on GrapheneOS than on stock Android, because they are not asking for privileged access they should not have.

## The F-Droid caveat

One difference is worth knowing before you choose a build. Bitwarden's official F-Droid build **excludes Firebase Messaging**, so live sync notifications do not work: the vault updates when you open the app or sync manually. That is a deliberate trade to keep the F-Droid build free of Play dependencies, not a bug.

If you want push sync, install the Play Store build. Both are official; the difference is the messaging dependency.

## Technical detail

No attestation requirement, no Play Services dependency, no integrity check. The app talks to Bitwarden's servers over the network and stores an encrypted vault locally.

The one thing worth doing is enabling biometric unlock, which uses the device's own keystore rather than a Google service, so it works unchanged.

**A note on sourcing.** This entry previously cited a forum thread about WhatsApp notifications, which has nothing to do with Bitwarden. That was a bad citation and it has been replaced with the app's own F-Droid repository.
