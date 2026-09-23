---
title: Revolut
slug: revolut
package: com.revolut.revolut
developer: Revolut
service_type: banking
countries: [GB, FR, DE, NL, ES, IT, SE, AT, CH]
requires_play_services: true
links:
  homepage: https://www.revolut.com
  play_store: https://play.google.com/store/apps/details?id=com.revolut.revolut
  fdroid: null
alternatives:
  - kind: in-person
    label: A bank that does not check the device
    covers: full
    detail: "Plenty of banks do not inspect the operating system at all. The community-maintained compatibility list tracks which banks work, country by country, and it is the fastest way to find one for yours."
    url: https://privsec.dev/posts/android/banking-applications-compatibility-with-grapheneos/
  - kind: browser
    label: Revolut's web app
    covers: partial
    detail: "web.revolut.com gives balances, statements, transfers, card controls and top-ups."
    limitation: "Revolut treats the web app as a fallback rather than a full client. Some flows push you back to the phone, and it is not a way to sign up."
    url: https://www.revolut.com/
reports:
  - date: 2026-09-10
    build: null
    device: null
    profile: null
    country: GB
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://privsec.dev/posts/android/banking-applications-compatibility-with-grapheneos/"
  - date: 2026-09-02
    build: null
    device: null
    profile: null
    country: GB
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://github.com/PrivSec-dev/banking-apps-compat-report/issues/90"
  - date: 2026-08-06
    build: null
    device: null
    profile: null
    country: GB
    play: sandboxed
    result: broken
    blocked_reason: play-integrity
    fixability: possible-via-workaround
    workaround: "Sign in to a throwaway Google account first, then install Revolut through the sandboxed Play Store. GrapheneOS reported that this worked for most users while it worked on a proper fix."
    tier: imported
    source: "https://cybernews.com/privacy/grapheneos-says-revolut-is-blocking-users-again-and-this-time-its-personal/"
---

Revolut works on GrapheneOS. It has been broken twice by Revolut's own device checks, and the second episode cleared in September 2026 with an app update.

**An earlier version of this entry said Revolut blocks your account, not just your phone, and told readers to expect a factory reset to stock.** That is not what the source it cited says, and it has been removed. The reports were about the app refusing to run and logins failing — device-level blocks. Nobody in the record describes Revolut closing an account over GrapheneOS. Treating an unsupported claim as the board's most serious warning was the wrong call, and it is corrected here rather than quietly edited away.

## The pattern

Revolut's checks come and go, and each cycle looks the same: the app stops working, the community finds a workaround, Revolut changes something, and it starts working again.

- **January 2025.** Revolut first blocks the OS. A community workaround is found.
- **August 2026.** GrapheneOS says publicly that Revolut has added checks aimed specifically at its build characteristics, beyond ordinary Play Integrity. A workaround is published, and the project says a fix is in development.
- **September 2026.** An app update resolves it. The reporter's read is that this was an A/B test that broke more than just GrapheneOS users — some less common stock devices hit it too — and that it was reverted under pressure.

That last point is the interesting one. A break that also hits stock devices is a bug, not a policy. It is a different thing from an app that deliberately checks for custom firmware and refuses to run, and this entry is recorded as `works` on that basis.

## If it breaks again

The workaround that worked in August 2026 was to sign in to a throwaway Google account and then install Revolut through the sandboxed Play Store. If the app fails after an update, retry before concluding anything — twice now, the fix has arrived within weeks.

## Technical detail

The August 2026 episode was reported as Play Integrity plus checks on build characteristics unique to GrapheneOS. Play Integrity on its own is not the whole story: GrapheneOS passes the basic integrity check and fails the device-certification one, which is a deliberate policy choice by Google rather than a security finding about the OS.

Because Revolut enforces at the certification level, a bootloader relock does not help, and neither does installing sandboxed Play Services — the app is asking about the operating system's certification, not about whether Play is present.
