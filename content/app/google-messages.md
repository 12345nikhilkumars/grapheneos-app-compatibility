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
  - date: 2026-02-16
    build: null
    device: null
    profile: owner
    country: US
    carrier: T-Mobile
    play: sandboxed
    result: works-with-setup
    blocked_reason: carrier-provisioning
    fixability: possible-with-steps
    workaround: "Turn on the Play services ICC authentication toggle, added in release 2026021200. Without it, RCS registration fails on carriers that require ICC auth."
    tier: imported
    source: "https://github.com/GrapheneOS/os-issue-tracker/issues/6173"
---

Google Messages works for SMS and MMS. The app runs, messages send, and nothing crashes.

**RCS** — the modern replacement for SMS, with typing indicators, read receipts, large images and end-to-end encryption in one-to-one chats — has a history of working, then not working, then partly working again. That history now has a resolution, which is more than this entry used to be able to say.

## What happened, in order

- **September 2025.** RCS registration broke for GrapheneOS users. The cause was traced to carriers requiring ICC authentication, which the sandboxed Play Services setup did not provide.
- **Late 2025.** Most carriers were restored by other means.
- **February 2026.** A proper fix shipped in release `2026021200` as a user-facing toggle for Play services ICC authentication. This resolved it for T-Mobile and AT&T, the two carriers that had held out.

So the current state is: SMS and MMS work unaided, and RCS works once the ICC authentication toggle is on. If RCS is still failing for you, that toggle is the first thing to check.

## Technical detail

RCS registration depends on a handshake between the carrier, Google's Jibe backend, and the device. The failure was never a Play Integrity block — the app was not being rejected for running a modified OS. It was a provisioning problem, which is why it came and went, and why it affected some carriers and not others.

That distinction is the reason this entry stayed as `unknown` for a long time. A provisioning problem looks like a compatibility problem from the outside, and guessing at the mechanism would have sent people to fix the wrong thing.

If RCS matters to you, check the current state before relying on it. Do not assume it works because it worked three months ago — and equally, do not assume it is broken because it broke last year.
