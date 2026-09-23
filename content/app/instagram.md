---
title: Instagram
slug: instagram
package: com.instagram.android
developer: Meta
service_type: social
global: true
requires_play_services: true
links:
  homepage: https://www.instagram.com
  play_store: https://play.google.com/store/apps/details?id=com.instagram.android
  fdroid: null
reports:
  - date: 2026-09-10
    build: "2026091000"
    device: pixel-9
    profile: owner
    country: GB
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/8330-app-compatibility"
---

Instagram works. Feed, stories, reels, DMs, and uploads all behave as they do on a stock device.

Push notifications depend on the same delivery path as other apps, so if they arrive late, the battery exception described on the Signal entry is the thing to try.

## Technical detail

No integrity check, no attestation requirement. Meta's consumer apps have not adopted device attestation the way payment and banking apps have, which is why they generally work without intervention.

The app requires Play Services for push notifications and some account features, satisfied by the sandboxed install.

Worth noting for anyone choosing between social apps on privacy grounds: Instagram working does not mean it is behaving. The app is functional on GrapheneOS; that is a separate question from what it collects once running.
