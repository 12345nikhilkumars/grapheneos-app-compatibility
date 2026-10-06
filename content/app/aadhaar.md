---
title: Aadhaar
slug: aadhaar
package: in.gov.uidai.pehchaan
developer: Unique Identification Authority of India
service_type: government
countries: [IN]
requires_play_services: true
links:
  homepage: https://myaadhaar.uidai.gov.in
  play_store: https://play.google.com/store/apps/details?id=in.gov.uidai.pehchaan
  fdroid: null
alternatives:
  - kind: browser
    label: The myAadhaar portal
    covers: partial
    detail: "myaadhaar.uidai.gov.in covers Aadhaar services in a browser: downloading e-Aadhaar, checking update status, and most profile changes."
    limitation: "No offline QR verification and no face authentication, which are the two things this app mainly exists for. It also needs a connection, where the app is built to work without one."
    url: https://myaadhaar.uidai.gov.in/
  - kind: hardware
    label: The physical card or an e-Aadhaar PDF
    covers: partial
    detail: "A printed Aadhaar card or a downloaded e-Aadhaar PDF is accepted wherever a physical document is accepted."
    limitation: "It cannot produce a verification QR or a digitally signed credential, so it does not replace the app for a verifier that requires one."
    url: null
reports:
  - date: 2026-09-24
    build: null
    device: pixel-10a
    profile: owner
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: play-integrity
    fixability: unknown
    workaround: null
    tier: maintainer
    reporter: "@12345nikhilkumars"
---

The Aadhaar app does not work on GrapheneOS. It calls the Play Integrity API, the check fails, and it stops with a generic error rather than naming the reason.

This is attestation rather than a fault in the app. The verdict is decided on Google's servers from the device's integrity signals, so no local setting changes it. Relocking the bootloader does not help either, which is what separates this from the apps that an exploit protection toggle fixes.

No workaround is known.
