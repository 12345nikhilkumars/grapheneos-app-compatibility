---
title: Gadgetbridge
slug: gadgetbridge
package: nodomain.freeyourgadget.gadgetbridge
developer: Freeyourgadget
service_type: wearables
global: true
requires_play_services: false
links:
  homepage: https://gadgetbridge.org
  play_store: null
  fdroid: https://f-droid.org/packages/nodomain.freeyourgadget.gadgetbridge/
reports:
  - date: 2026-09-10
    build: "2026091000"
    device: pixel-9
    profile: owner
    country: DE
    play: none
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: community
    reporter: "@grapheneos-forum"
    source: "https://discuss.grapheneos.org/d/15249-galaxy-wearable-install-failure"
---

Gadgetbridge is the reason a smartwatch is not a blocker on GrapheneOS. It talks to a long list of watches and fitness bands directly, with no vendor app and no cloud account.

This matters because the official companion apps are a weak point. Samsung's Galaxy Wearable is reported to fail partway through installation on GrapheneOS, and the usual suggestion is to use Gadgetbridge with a watch it supports instead.

Check the supported device list before buying a watch for this purpose. Support is broad but not universal, and it is better to confirm the specific model first than to discover the gap afterwards.

## Technical detail

Gadgetbridge speaks the vendor's Bluetooth protocol directly rather than going through the manufacturer's app and cloud service. That removes the Play Services dependency entirely, and it also means notifications, calls, and health data stay on the phone.

The trade-off is fidelity. Vendor apps typically offer firmware updates, some advanced sensors, and cloud sync that Gadgetbridge either does not implement or implements partially for a given model. What works varies by watch, so the supported-devices list is the thing to read.
