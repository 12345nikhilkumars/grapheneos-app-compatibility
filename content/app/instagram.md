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
reports: []
---

Instagram is expected to work — feed, stories, reels, DMs, and uploads behaving as they do on a stock device.

**Nobody has filed a report for this app.** The expectation comes from the absence of any device integrity check in Meta's consumer apps, not from a test recorded here. The previous version of this entry cited a forum thread that does not mention Instagram, which is not evidence, and it has been removed.

## Why it is expected to work

Instagram requires Play Services for push notifications and some account features, satisfied by the sandboxed install. It does not call Play Integrity, and Meta has not adopted device attestation in its consumer apps the way payment and banking apps have.

Push notifications depend on the same delivery path as other apps, so if they arrive late, the battery exception described on the Signal entry is the thing to try.

## A note that is not about compatibility

Instagram working does not mean it is behaving. The app is functional on GrapheneOS; that is a separate question from what it collects once running, and it is worth not confusing the two. A privacy-focused OS limits what an app can reach on the device, but it cannot change what the app sends to its own servers once you sign in.

If you want a report to exist for this app, running it and writing down what happened is enough.
