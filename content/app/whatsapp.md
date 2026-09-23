---
title: WhatsApp
slug: whatsapp
package: com.whatsapp
developer: Meta
service_type: messaging
global: true
requires_play_services: true
links:
  homepage: https://www.whatsapp.com
  play_store: https://play.google.com/store/apps/details?id=com.whatsapp
  fdroid: null
reports:
  - date: 2026-09-05
    build: "2026090500"
    device: pixel-8
    profile: owner
    country: IN
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/13911-whatsapp-notifications"
---

WhatsApp works. Messages send and receive, calls connect, media transfers, and the app behaves the same as it does on a stock Pixel.

Two things are worth knowing.

**Notifications** rely on the same push delivery that affects other messengers. If messages arrive late, the fix is the battery exception described on the Signal entry — it is not specific to WhatsApp.

**Chat backups to Google Drive** will not work, because that feature depends on Google Drive integration that is not present. Local backups still work, and you can export a chat manually. If your backup habit depends on Drive, change it before you migrate, not after.

## Technical detail

The app requires Play Services, and the sandboxed Play Services installs satisfy that requirement without granting Google any privileged access.

No attestation check blocks WhatsApp itself. Reports of WhatsApp refusing to run are almost always reports of a *different* problem — most often the UPI payments feature inside WhatsApp, which is a separate integration with its own restrictions and is covered under the India payment entries.
