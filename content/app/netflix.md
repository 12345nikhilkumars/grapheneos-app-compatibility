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
alternatives:
  - kind: browser
    label: Netflix on a computer
    covers: full
    detail: "The website plays the same catalogue at the resolution your subscription allows. This is the reliable route if anything about playback on the phone is wrong."
    url: https://www.netflix.com/
reports:
  - date: 2023-10-25
    build: "2023102300"
    device: pixel-7-pro
    profile: owner
    country: GB
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://discuss.grapheneos.org/d/7981-netflix-users-wait"
---

Netflix installs, signs in, and plays, including at the higher resolutions your subscription allows. GrapheneOS supports Widevine L1 on Pixels.

**This entry used to say the opposite, and it was wrong.** It claimed playback was permanently capped at Widevine L3 (roughly 480p) and that nothing could lift it. That described a real problem, but it was a bug in one 2023 release rather than a permanent limitation, and it had already been fixed when the entry was written.

## What actually happened

The Android 14 update in October 2023 dropped affected devices from Widevine L1 to L3. It was reported on the forum, acknowledged as a known issue, tracked as a GrapheneOS bug, and fixed in release `2023102300`. The release notes for that build read:

> Pixel 6, Pixel 6 Pro, Pixel 6a, Pixel 7, Pixel 7 Pro, Pixel 7a, Pixel Tablet, Pixel Fold: fix support for Widevine L1 on Android 14

Anyone who updated and still saw L3 was told to clear the Netflix app's storage, which resolved it.

## Technical detail

Widevine has three security levels. L1 requires a hardware-backed trusted execution path, and GrapheneOS provides one on Pixels: DRM support is enabled in the OS, with Widevine certificate provisioning going through a GrapheneOS reverse proxy by default. There is a **Settings → Network & Internet → Widevine provisioning** switch if you would rather use Google's service directly.

Two things are worth separating, because they get conflated:

- **L1 availability** is an OS capability. GrapheneOS has it on supported Pixels.
- **What a specific app does with it** is the app's business. Netflix also gates some features on other checks.

One limitation that is real: DRM is disabled in Vanadium, GrapheneOS's own browser, so protected video will not play there. It works in other browsers and in the app.

## Why this report is dated 2023

The report above carries the date of the fix, not a recent test, and the board flags it as possibly out of date because of that. That is deliberate. Nobody has filed a current report confirming Netflix behaviour on an Android 17 build, so the honest position is: this was fixed, and it should be re-checked. If you use Netflix on a current build, a report would replace a three-year-old one.
