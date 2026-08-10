---
title: Graceful stream validation
description: 'When adding or updating playlist entries, treat common failure causes
  explicitly: validate identifiers and supported URL/source formats up front, and
  gracefully degrade for expected runtime failures.'
repository: iptv-org/iptv
label: Error Handling
language: Other
comments_count: 3
repository_stars: 135586
---

When adding or updating playlist entries, treat common failure causes explicitly: validate identifiers and supported URL/source formats up front, and gracefully degrade for expected runtime failures.

Apply two checks:
1) Pre-validate metadata and input type
- tvg-id/channel identifiers must be valid and map to an accepted channel definition (avoid “Invalid channel ID”).
- Only allow supported source URL types; reject known non-accepted formats (e.g., Xtream-Codes).

2) Gracefully handle expected runtime failures
- If a stream is known to fail due to policy/geo restrictions (e.g., HTTP 451), do not leave a “normal-looking” working entry. Annotate it as failing and include the reason so consumers can skip it or present it correctly.

Example (m3u-style annotation):
```m3u
#EXTINF:-1 tvg-id="Channel8.th",Channel 8 (720p) [Geo-blocked]
# 451 Not Available Due To Legal Reasons outside of Thailand.
https://example.com/geo-blocked/stream.m3u8
```

Result: fewer avoidable errors (bad IDs, unsupported formats) and clearer, actionable behavior for unavoidable failures (explicit geo-block markers instead of silent breakage).