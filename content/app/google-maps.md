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
reports:
  - date: 2026-09-10
    build: "2026091000"
    device: pixel-8
    profile: owner
    country: US
    play: sandboxed
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/8330-app-compatibility"
---

Google Maps works, including navigation, live traffic, and saved places. It needs Play Services, and the sandboxed install satisfies that requirement without giving Google privileged access to the device.

This surprises people who expect anything Google-branded to be blocked. The distinction is that Maps wants Play Services for location and account features, but it does not demand a hardware attestation that the OS is unmodified.

Location accuracy is unchanged. GrapheneOS does not degrade the location stack; it only gives you more granular control over which apps can reach it.

## Technical detail

The app uses Play Services for the Maps SDK, account sign-in, and location services. Sandboxed Play Services provides all three as an ordinary app, which is sufficient here.

If Maps fails to get a location fix, the usual cause is that Play Services itself has been denied location permission — check the sandboxed Play Services entry in Settings rather than the Maps entry, because the permission is held one level down.

Alternatives such as Organic Maps work without Play Services at all, at the cost of live traffic data.
