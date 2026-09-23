---
title: Signal
slug: signal
package: org.thoughtcrime.securesms
developer: Signal Foundation
service_type: messaging
global: true
requires_play_services: true
links:
  homepage: https://signal.org
  play_store: https://play.google.com/store/apps/details?id=org.thoughtcrime.securesms
  fdroid: null
reports:
  - date: 2026-09-05
    build: "2026090500"
    device: pixel-8
    profile: owner
    country: DE
    play: sandboxed
    result: works-degraded
    blocked_reason: push-delivery
    fixability: possible-with-steps
    workaround: "Grant Signal an unrestricted battery exception under Settings, Apps, Signal, Battery. Without it, notifications can be delayed by hours."
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/25079-signal-notifications-delayed"
  - date: 2026-07-15
    build: "2026071500"
    device: pixel-9
    profile: secondary
    country: DE
    play: sandboxed
    result: works-degraded
    blocked_reason: push-delivery
    fixability: possible-with-steps
    workaround: "Set Signal's battery usage to unrestricted."
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://github.com/GrapheneOS/os-issue-tracker/issues/6034"
---

Signal itself works. Messages send and receive, calls connect, and nothing about the app is broken.

The problem is **when you find out a message arrived**. Notifications can be delayed by minutes or hours, and in the worst reports they do not arrive until you open the app. For a messenger people rely on for time-sensitive things, this is the failure that matters.

The fix is a battery setting, not an app change, and it usually holds. It is the first thing to try if notifications are unreliable.

## Technical detail

Push notifications arrive through Firebase Cloud Messaging, which is delivered by the sandboxed Play Services. Android's battery optimisation is aggressive about background work, and a sandboxed Play Services process is more likely to be deprioritised than a privileged system one.

Marking Signal as unrestricted stops the system from suspending its background delivery. Note that this is per-app, and other messengers will need the same treatment.

If notifications still lag after that, check that sandboxed Play Services itself has not been battery-restricted — the app cannot receive anything Play Services never delivered.
