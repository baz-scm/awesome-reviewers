---
title: Avoid Tokenized Stream URLs
description: Do not include ephemeral authentication parameters (e.g., `session=`,
  `tkn=`, `hash=`, `sign=`) or other provider-specific auth wrappers in static `.m3u`
  entries. These links commonly expire (“timebomb”) and/or may be IP-locked, causing
  playback failures and turning the playlist into a security-sensitive artifact. Also,
  reject/omit link types your system...
repository: iptv-org/iptv
label: Security
language: Other
comments_count: 9
repository_stars: 135586
---

Do not include ephemeral authentication parameters (e.g., `session=`, `tkn=`, `hash=`, `sign=`) or other provider-specific auth wrappers in static `.m3u` entries. These links commonly expire (“timebomb”) and/or may be IP-locked, causing playback failures and turning the playlist into a security-sensitive artifact. Also, reject/omit link types your system explicitly disallows (e.g., Xtream-Codes / “x-stream codes”). If a source is access-restricted, label it (e.g., `[Geo-blocked]`, `[403]`) and, when multiple streams are required (audio/video split or multi-region variants), document the composition so players know what to use.

Practical rules:
- Prefer plain, non-expiring HLS master/variant URLs without per-user/per-session query params.
- If a link requires `session=`, `tkn=`, `hash=`, or similar: do not bake it into the playlist; instead, store/generate it at request time (server-side) or obtain a stable master URL.
- If the entry is disallowed (Xtream-Codes / x-stream codes), remove it entirely.
- When you expect restricted access, reflect it in `#EXTINF` text (e.g., `... [Geo-blocked]`) rather than shipping a failing link without context.

Example (bad → avoid tokens):
```m3u
#EXTINF:-1 tvg-id="Some.Ch" ,Some Channel
https://example.com/live/stream.m3u8?session=ABC123
```

Example (good → stable URL + clear restriction):
```m3u
#EXTINF:-1 tvg-id="Some.Ch" ,Some Channel [Geo-blocked]
https://example.com/live/stream.m3u8
```