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
  - date: 2026-08-01
    build: null
    device: pixel-9
    profile: owner
    country: DE
    play: none
    result: works
    blocked_reason: none
    fixability: not-applicable
    workaround: null
    tier: imported
    source: "https://discuss.grapheneos.org/d/15249-graphene-and-smart-watches"
---

Gadgetbridge is the reason a smartwatch is not automatically a blocker on GrapheneOS. It talks to a long list of watches and fitness bands directly, with no vendor app and no cloud account.

This matters because the official companion apps are the weak point. Samsung's Galaxy Wearable is repeatedly reported to fail on GrapheneOS, and the usual suggestion is to use Gadgetbridge with a watch it supports instead.

**How strong is that Galaxy Wearable claim?** Moderate, and the entry used to imply it was settled. The reports cluster on the GrapheneOS forum and are mostly older. The failure mode described is permissions and notification bridging rather than the install failing outright, which means it is the kind of thing an app update can change. Test your own watch rather than assuming.

Check the supported device list before buying a watch for this purpose. Support is broad but not universal, and it is better to confirm the specific model first than to discover the gap afterwards.

## Technical detail

Gadgetbridge speaks the vendor's Bluetooth protocol directly rather than going through the manufacturer's app and cloud service. That removes the Play Services dependency entirely, and it also means notifications, calls, and health data stay on the phone.

The trade-off is fidelity. Vendor apps typically offer firmware updates, some advanced sensors, and cloud sync that Gadgetbridge either does not implement or implements partially for a given model. What works varies by watch, so the supported-devices list is the thing to read.

Worth noting: Gadgetbridge works without Play Services, which makes it a rare case where the GrapheneOS answer is also the better answer on a stock phone.
