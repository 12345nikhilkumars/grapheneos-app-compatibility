---
title: Google Messages
slug: google-messages
package: com.google.android.apps.messaging
developer: Google
service_type: messaging
global: true
requires_play_services: true
links:
  homepage: https://messages.google.com
  play_store: https://play.google.com/store/apps/details?id=com.google.android.apps.messaging
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
    source: "https://github.com/GrapheneOS/os-issue-tracker/issues/6173"
---

Google Messages works for SMS and MMS. The app runs, messages send, and nothing crashes.

**RCS is the part that breaks.** RCS is the modern replacement for SMS — typing indicators, read receipts, large images, end-to-end encryption in one-to-one chats. On GrapheneOS it has a history of working, then not working, then partly working again.

As of this report the situation is unstable: some people can receive RCS messages but not send them, and others cannot register at all. Because this has flip-flopped more than once, treat any specific claim about it as needing a current date attached.

## Technical detail

RCS registration depends on a handshake between the carrier, Google's Jibe backend, and the device. In September 2025 a change on Google's side broke registration for GrapheneOS, and a partial fix followed in early 2026.

The failure is not a Play Integrity block — the app is not being rejected for running a modified OS. It is a provisioning problem, which is why it sometimes works and sometimes does not, and why the status here is recorded as `unknown` rather than given a confident reason.

If RCS matters to you, check the current state before relying on it. Do not assume it works because it worked three months ago.
