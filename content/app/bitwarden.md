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
reports:
  - date: 2026-09-10
    build: "2026091000"
    device: pixel-8
    profile: owner
    country: US
    play: none
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/13911-whatsapp-notifications"
---

Bitwarden works fully, and it is one of the apps that runs best on GrapheneOS because it does not need Play Services at all.

Autofill, biometric unlock, sync, and the browser extension pairing all behave normally. It is available on F-Droid as well as the Play Store, so you can install it without sandboxed Play Services if you prefer.

This entry is included as a counterweight to the broken ones. Most apps work, and password managers are a category where the privacy-focused options are actively better on GrapheneOS than on stock Android, because they are not asking for privileged access they should not have.

## Technical detail

No attestation requirement, no Play Services dependency, no integrity check. The app talks to Bitwarden's servers over the network and stores an encrypted vault locally.

The one thing worth doing is enabling biometric unlock, which uses the device's own keystore rather than a Google service, so it works unchanged.
