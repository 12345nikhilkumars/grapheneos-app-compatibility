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
alternatives:
  - kind: app
    label: Molly
    covers: full
    detail: "A hardened Signal fork, and a drop-in replacement for the same account. The FOSS build uses UnifiedPush instead of Firebase Cloud Messaging, so notifications do not go through sandboxed Play Services at all."
    url: https://molly.im/
  - kind: other
    label: Remove Play Services entirely
    covers: partial
    detail: "Users who installed no Play Services at all report notifications behaving normally, because there is no sandboxed process for the battery manager to suspend."
    limitation: "Only viable if you do not need any app that requires Play Services, which rules it out for most people."
    url: null
reports:
  - date: 2025-08-01
    build: null
    device: pixel-8
    profile: owner
    country: DE
    play: sandboxed
    result: works-degraded
    blocked_reason: push-delivery
    fixability: possible-with-steps
    workaround: "Set battery usage to unrestricted for both Signal and sandboxed Google Play Services. This reduces the delay for most people. It does not eliminate it for everyone."
    tier: imported
    source: "https://github.com/GrapheneOS/os-issue-tracker/issues/6034"
---

Signal itself works. Messages send and receive, calls connect, and nothing about the app is broken.

The problem is **when you find out a message arrived**. Notifications can be delayed by minutes or hours, and in the worst reports they do not arrive until you open the app. For a messenger people rely on for time-sensitive things, that is the failure that matters.

The usual fix is a battery setting, and it usually helps. **It is not a reliable fix, though**, and this entry used to oversell it. Users who had already set the battery exception still reported delays of hours, and the GrapheneOS issue tracking the problem was closed without a fix rather than solved.

## Technical detail

Push notifications arrive through Firebase Cloud Messaging, delivered by the sandboxed Play Services. Android's battery optimisation is aggressive about background work, and a sandboxed Play Services process is more likely to be deprioritised than a privileged system one.

Marking **both** Signal and sandboxed Play Services as unrestricted is the first thing to try. Both matter: if Play Services is suspended, the app cannot receive anything that was never delivered. This is per-app, so other messengers need the same treatment.

If that does not settle it, the honest answer is that you are depending on a delivery path GrapheneOS cannot fully control. The alternatives above are the ways out: Molly, which uses UnifiedPush rather than FCM, or removing Play Services altogether.

## Worth knowing

This is not an app compatibility problem, and it is not specific to Signal. Every app that relies on push through sandboxed Play Services is on the same path. Signal is the entry where it gets discussed because it is the app where late notifications cost the most.
