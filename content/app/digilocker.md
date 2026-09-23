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
reports: []
---

DigiLocker holds government-issued documents in digital form: driving licence, PAN, vehicle registration, academic certificates. If it stops working, it takes your documents with it, which makes it one of the higher-stakes apps to test before committing to a new phone.

**Nobody has reported testing this, and the search for existing reports came up empty too.** It is listed because it matters, not because there is an answer here.

That absence is itself the finding. DigiLocker appears in no GrapheneOS forum thread, no issue, and no community compatibility list. Either very few GrapheneOS users in India depend on it, or the ones who do have not written it down.

If you run GrapheneOS in India and use DigiLocker, a report would be genuinely useful. In particular: whether the app launches, whether existing documents still display, and whether Aadhaar-based sign-in completes.

## Technical detail

Government identity apps in India have tended to be stricter about device integrity than banking apps, and several use Aadhaar authentication flows that involve their own device checks. That makes this a plausible failure, but plausible is not the same as known, which is exactly why the entry is empty rather than guessed at.

An entry with no reports is a valid state. It says the app is known to matter and unknown in practice, which is more useful than a fabricated status.

## What to do in the meantime

The website is the fallback while this is unknown, and it covers reading and downloading your documents. Keep a printed or offline copy of anything you might need urgently (a licence or an insurance certificate) before you rely on the app on any phone, GrapheneOS or not.
