---
title: HDFC Bank
slug: hdfc-bank
package: com.snapwork.hdfc
developer: HDFC Bank
service_type: banking
countries: [IN]
requires_play_services: true
links:
  homepage: https://www.hdfcbank.com
  play_store: https://play.google.com/store/apps/details?id=com.snapwork.hdfc
  fdroid: null
reports:
  - date: 2026-09-10
    build: "2026091000"
    device: pixel-8
    profile: owner
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: not-possible
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/37215-indian-upi-apps"
  - date: 2026-07-15
    build: "2026071500"
    device: pixel-8
    profile: owner
    country: IN
    play: sandboxed
    result: broken
    blocked_reason: custom-firmware-detection
    fixability: not-possible
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/26888-india-app-compatibility"
---

The HDFC app detects that the operating system is not stock and refuses to proceed. There is no error code to work around and no setting that changes it.

Both the older app and the newer replacement behave the same way, which suggests the check was added deliberately rather than being a side effect of a security library.

**Net banking in a browser still works.** That is the practical fallback, and for most day-to-day banking it is sufficient.

## Technical detail

HDFC's app performs its own device integrity check rather than relying solely on Play Integrity, which is why the failure message names the firmware rather than reporting an attestation failure. Because the check is in the app and enforced server-side, there is nothing to configure around it.

Two community reports, two months apart, with the same result and no known workaround. The `not-possible` verdict reflects that, not a lack of effort.
