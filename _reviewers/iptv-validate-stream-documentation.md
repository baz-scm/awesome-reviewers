---
title: Validate stream documentation
description: When updating playlist/stream documentation (e.g., .m3u EXTINF entries),
  ensure **both the URL and the metadata follow the documented stream-description
  scheme** and are **not based on player-specific behavior**.
repository: iptv-org/iptv
label: Documentation
language: Other
comments_count: 3
repository_stars: 135586
---

When updating playlist/stream documentation (e.g., .m3u EXTINF entries), ensure **both the URL and the metadata follow the documented stream-description scheme** and are **not based on player-specific behavior**.

Apply:
- **Verify the link**: confirm it resolves and plays using a neutral test (don’t assume a specific player build/version). If a URL is broken, fix the endpoint.
- **Use the correct HLS/M3U endpoint**: prefer the scheme’s recommended manifest (e.g., a `master.m3u8` manifest) rather than a chunklist URL unless the scheme explicitly requires it.
- **Follow the EXTINF schema**: ensure `tvg-id`, `tvg-name`/display name, and grouping fields are populated consistently.
- **Add required labels in EXTINF**:
  - If the stream is **not 24/7**, include the corresponding reliability label.
  - If access is **region-limited**, add **[Geo-blocked]**.
- **Avoid player-version-only claims**: don’t add alternatives that only work on one specific player/version; if behavior differs, capture it via the scheme labels.

Example (pattern):
```m3u
#EXTINF:-1 tvg-id="SABC1.za" tvg-name="SABC 1" group-title="News" [not 24/7] SABC 1 (720p)
https://example.cdn/sabc1/master.m3u8

#EXTINF:-1 tvg-id="XYZ.za" tvg-name="XYZ TV" group-title="General" [Geo-blocked] XYZ TV
https://example.cdn/xyz/master.m3u8
```