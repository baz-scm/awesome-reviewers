---
title: M3U metadata and links
description: When editing M3U playlist configuration, treat each `#EXTINF` block as
  configuration data that must be (1) internally consistent, (2) externally valid,
  and (3) quality/behavior-preserving.
repository: iptv-org/iptv
label: Configurations
language: Other
comments_count: 4
repository_stars: 135586
---

When editing M3U playlist configuration, treat each `#EXTINF` block as configuration data that must be (1) internally consistent, (2) externally valid, and (3) quality/behavior-preserving.

Apply this checklist:
- **Keep `tvg-id` and display name consistent**: use the correct channel identifier and naming convention; ensure any quality marker in the identifier matches what the entry actually represents.
- **Verify the URL works**: don’t leave broken endpoints. If a provider changes an endpoint, update to a known-good variant (e.g., switching between `index.m3u8` and `index_1.m3u8`).
- **Preserve adaptive streams when possible**: if the source provides an adaptive URL, avoid unnecessary replacements that remove adaptive behavior.

Example pattern (correctness + naming + working endpoint):
```m3u
#EXTINF:-1 tvg-id="DespertarTV.br@HD",Despertar TV (720p)
https://example-provider.com/path/playlist.m3u8

# If an endpoint breaks, switch to a known-good variant:
# (do this only after verification)
#EXTINF:-1 tvg-id="MBCPersia.ae",MBC Persia (1080p)
https://shls-mbcpersia-prod-dub.shahid.net/out/v1/<token>/index_1.m3u8
```

Use this as a review gate: changes to playlists must include evidence (or at least a verification step) that the URL is reachable and that the metadata (`tvg-id`/label) matches the intended stream identity.