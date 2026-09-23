---
title: Android Auto
slug: android-auto
package: com.google.android.projection.gearhead
developer: Google
service_type: transport
global: true
requires_play_services: true
links:
  homepage: https://www.android.com/auto/
  play_store: https://play.google.com/store/apps/details?id=com.google.android.projection.gearhead
  fdroid: null
reports:
  - date: 2026-08-20
    build: "2026081300"
    device: pixel-8
    profile: owner
    country: US
    play: sandboxed
    result: works-degraded
    blocked_reason: unknown
    fixability: unknown
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/37131-android-auto-wireless"
---

Android Auto works over a cable. Wireless Android Auto is the problem.

The reported symptom is that it will not reconnect automatically, and when it does connect it drops every few minutes. For anyone used to getting in the car and having it just work, that is a significant downgrade.

Wired connections have a history of smaller quirks but are generally reliable, so a cable is the practical answer while this is unresolved.

## Technical detail

This is not an attestation block — Android Auto does not check device integrity. The regression appeared with the Android 17 base and affects wireless projection specifically, which points at the Wi-Fi handshake or the projection service rather than at anything GrapheneOS changed deliberately.

A fix was merged upstream but reports of the problem continued after it. Because the status is genuinely unsettled and there is no confirmed workaround, `fixability` is recorded as `unknown` rather than `not-possible` — a merged fix that has not fully landed is not the same as an unfixable problem.

If you depend on wireless Android Auto, test it before switching, and test the wireless path specifically rather than assuming a cable result carries over.
