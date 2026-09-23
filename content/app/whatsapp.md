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
    build: null
    device: pixel-8
    profile: owner
    country: IN
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://discuss.grapheneos.org/d/19889-whatsapp-restore"
---

WhatsApp works. Messages send and receive, calls connect, media transfers, and the app behaves the same as it does on a stock Pixel.

Two things are worth knowing.

**Notifications** rely on the same push delivery that affects other messengers. If messages arrive late, the battery exception described on the Signal entry is the thing to try. It is not specific to WhatsApp.

**Chat backups to Google Drive** work, but only if you set them up in the right order. This entry used to say they do not work at all, which was wrong. Install sandboxed Play Services and Google Drive, sign in to both, and only then install WhatsApp. If you install WhatsApp first, the backup option does not appear. Local backups work regardless, and you can export a chat manually.

## Technical detail

The app requires Play Services, and the sandboxed Play Services installs satisfy that requirement without granting Google any privileged access.

No attestation check blocks WhatsApp itself. Reports of WhatsApp refusing to run are almost always reports of a *different* problem, most often the UPI payments feature inside WhatsApp, which is a separate integration with its own restrictions and is covered under the India payment entries.

The Drive backup detail is a good example of why this board asks for the build and the setup rather than just a verdict. "It works" and "it does not work" were both being reported by people who were right about their own phone, and the difference was install order.
