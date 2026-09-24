---
title: DigiLocker
slug: digilocker
package: com.digilocker.android
developer: National e-Governance Division
service_type: government
countries: [IN]
requires_play_services: true
links:
  homepage: https://www.digilocker.gov.in
  play_store: https://play.google.com/store/apps/details?id=com.digilocker.android
  fdroid: null
alternatives:
  - kind: browser
    label: The DigiLocker website
    covers: partial
    detail: "digilocker.gov.in gives you access to your issued documents, and you can download and print them. Aadhaar-based sign-in works through a browser."
    limitation: "Some issuers and some verification flows only accept documents presented in the app, and the app is what most people need when they are asked to show a document at a counter."
    url: https://www.digilocker.gov.in/
reports:
  - date: 2026-09-24
    build: "2026091901"
    device: pixel-10a
    profile: owner-private-space
    country: IN
    play: sandboxed
    result: works-with-setup
    blocked_reason: play-services-required
    fixability: possible-with-steps
    workaround: "Install Play Services and give permissions."
    tier: maintainer
    reporter: "@12345nikhilkumars"
---

DigiLocker holds government documents: driving licence, PAN, vehicle registration, academic certificates.

It needs Play Services, not a stock OS. Nothing about GrapheneOS stops it.

Keep a printed copy of anything urgent, a licence or an insurance certificate, before you rely on it.
