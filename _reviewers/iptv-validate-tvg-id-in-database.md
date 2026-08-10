---
title: Validate tvg-id In Database
description: Whenever you edit an M3U/M3U8 playlist entry with a `#EXTINF` line, ensure
  the `tvg-id` is consistent with the canonical channel database. If the `tvg-id`
  you intend to use does not exist in the database, either (a) leave `tvg-id` empty
  to avoid invalid metadata, or (b) submit/add the missing channel to the database
  first. Also, don’t assume one feed...
repository: iptv-org/iptv
label: Database
language: Other
comments_count: 5
repository_stars: 135586
---

Whenever you edit an M3U/M3U8 playlist entry with a `#EXTINF` line, ensure the `tvg-id` is consistent with the canonical channel database. If the `tvg-id` you intend to use does not exist in the database, either (a) leave `tvg-id` empty to avoid invalid metadata, or (b) submit/add the missing channel to the database first. Also, don’t assume one feed represents all variants: if the channel has multiple qualities/regions/logo versions (as reflected by database entries), add separate feeds per variant instead of reusing a single `tvg-id`.

Decision rule:
- `tvg-id` exists in database → use that exact `tvg-id`.
- `tvg-id` does not exist → leave `tvg-id=""` OR create the database entry (then update playlist).
- Different quality/region/version → create separate `#EXTINF` entries (and database entries as needed), not just one shared line.

Example (good vs. bad):
```m3u
# BAD: empty/unknown tvg-id
#EXTINF:-1 tvg-id="",Some Channel (1080p)
https://example.com/stream_1080p.m3u8

# BETTER: tvg-id matches a database entry
#EXTINF:-1 tvg-id="SomeChannel.xx",Some Channel (1080p)
https://example.com/stream_1080p.m3u8

# If you have another variant/quality that is distinct in the database:
#EXTINF:-1 tvg-id="SomeChannel.xx",Some Channel (720p)
https://example.com/stream_720p.m3u8
```