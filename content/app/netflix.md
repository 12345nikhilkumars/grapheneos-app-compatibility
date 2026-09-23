---
title: Netflix
slug: netflix
package: com.netflix.mediaclient
developer: Netflix
service_type: streaming
global: true
requires_play_services: false
links:
  homepage: https://www.netflix.com
  play_store: https://play.google.com/store/apps/details?id=com.netflix.mediaclient
  fdroid: null
reports:
  - date: 2026-08-20
    build: "2026081300"
    device: pixel-8
    profile: owner
    country: US
    play: sandboxed
    result: works-degraded
    blocked_reason: drm
    fixability: not-possible
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/7981-widevine-drm"
---

Netflix installs, signs in, and plays. Nothing is broken.

The catch is picture quality. Playback is capped at a low resolution regardless of your connection or your subscription tier, because the app cannot use the higher DRM security level. On a Pixel with a high-density display this is immediately obvious.

The same limitation applies to other DRM-protected streaming services, including Prime Video and most regional equivalents.

## Technical detail

Widevine has three security levels. L1 requires a hardware-backed trusted execution path that GrapheneOS cannot provide, so devices fall back to L3, which caps protected output at a low resolution.

This is a hardware and licensing limitation rather than a bug. No configuration change, app version, or update will lift it. The only practical options are watching on another device, or accepting the lower resolution.

Free, unencrypted content is unaffected — the cap applies only to DRM-protected streams.
