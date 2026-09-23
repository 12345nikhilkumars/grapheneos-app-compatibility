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
alternatives:
  - kind: hardware
    label: A phone mount and the phone's own maps
    covers: partial
    detail: "Google Maps or Organic Maps on the phone screen, in a mount, with the phone's own audio. Navigation works, and so does everything else the phone does."
    limitation: "No car display, no steering-wheel controls, no automatic audio switching, and no voice assistant through the car."
    url: null
reports:
  - date: 2026-08-20
    build: null
    device: pixel-8
    profile: owner
    country: US
    play: sandboxed
    result: works-degraded
    blocked_reason: unknown
    fixability: possible-with-steps
    workaround: "Run Android Auto in the owner profile. It frequently fails in a secondary profile or in Private Space. Wired connections are more reliable than wireless."
    tier: imported
    source: "https://discuss.grapheneos.org/d/37131-android-auto-wireless"
---

Android Auto is unreliable on GrapheneOS, and this entry previously understated that. It said wired connections work and only wireless is broken. A month-long independent review found Android Auto **"near-impossible to get to work regularly"**, and reports of wireless problems were still arriving in September 2026.

That is a wider failure than a wireless-specific regression, and it is worth planning around rather than treating as a minor quirk.

## What is reported

Symptoms vary. Some people get a connection that drops every few minutes. Some get one that will not reconnect automatically. Some cannot get it to start at all.

**Profile matters more than anything else here.** Android Auto needs to run in the owner profile. Reports of it failing in a secondary profile or in Private Space are common, and at least one user in the owner profile reports wireless working without trouble — which suggests some of the failures attributed to GrapheneOS are really failures in a non-owner profile.

If you are testing Android Auto, test it in the owner profile before concluding anything.

## Technical detail

This is not an attestation block — Android Auto does not check device integrity. The problems appeared around the Android 17 base and affect projection generally, which points at the Wi-Fi handshake or the projection service rather than at anything GrapheneOS changed deliberately.

A fix was merged upstream but reports continued afterwards. Because the status is genuinely unsettled and there is no confirmed fix, `fixability` is `possible-with-steps` rather than `not-possible`: the owner-profile requirement is a real, actionable step, and a merged fix that has not fully landed is not the same as an unfixable problem.

## If you depend on it

Test before you switch, and test the specific thing you rely on — a cable result does not tell you anything about the wireless path. If Android Auto is central to how you use your car, treat it as the riskiest item on this board after payments.
