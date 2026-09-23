---
title: Google Maps
slug: google-maps
package: com.google.android.apps.maps
developer: Google
service_type: transport
global: true
requires_play_services: true
links:
  homepage: https://maps.google.com
  play_store: https://play.google.com/store/apps/details?id=com.google.android.apps.maps
  fdroid: null
alternatives:
  - kind: app
    label: Organic Maps
    covers: partial
    detail: "Offline maps built on OpenStreetMap, with no Play Services and no account. Available on F-Droid, and it works well for driving and walking directions."
    limitation: "No live traffic, no live transit data, and business listings are thinner. For navigating somewhere you already know the route to, it is fine."
    url: https://organicmaps.app/
  - kind: browser
    label: maps.google.com
    covers: partial
    detail: "The full Maps experience in a browser, including traffic and transit."
    limitation: "No turn-by-turn navigation, and no offline maps."
    url: https://maps.google.com/
reports: []
---

Google Maps is expected to work, including navigation, live traffic, and saved places. It needs Play Services, and the sandboxed install satisfies that requirement without giving Google privileged access to the device.

**Nobody has filed a report for this app, though.** The paragraph above is based on how sandboxed Play Services generally behaves (GrapheneOS documents near-complete app compatibility through it), not on a test someone ran and recorded here. An earlier version of this entry carried a source link to a forum thread that does not mention Maps at all, which was not good enough. It has been removed rather than replaced with a guess.

If you use Maps on GrapheneOS, a report would close this out. It is a one-line contribution and it would replace an assumption with a fact.

## Why it is expected to work

Maps wants Play Services for the Maps SDK, account sign-in, and location services. None of those require the device to pass an integrity check. That is the distinction that matters on GrapheneOS: an app that *uses* Play Services usually works, and an app that *polices* the device usually does not. Maps is in the first group.

Location accuracy is unchanged. GrapheneOS does not degrade the location stack; it gives you more granular control over which apps can reach it.

## Technical detail

If Maps fails to get a location fix, the usual cause is that Play Services itself has been denied location permission. Check the sandboxed Play Services entry in Settings rather than the Maps entry, because the permission is held one level down.
