---
title: Use adaptive load-balanced streams
description: 'When adding/updating HLS stream URLs, pick the network endpoint that
  is most likely to work reliably:


  - Prefer adaptive HLS entrypoints (e.g., `master.m3u8`, `playlist.m3u8`, `manifest.m3u8`,
  `index.m3u8`) instead of redirect chains or single-bitrate links.'
repository: iptv-org/iptv
label: Networking
language: Other
comments_count: 9
repository_stars: 135586
---

When adding/updating HLS stream URLs, pick the network endpoint that is most likely to work reliably:

- Prefer adaptive HLS entrypoints (e.g., `master.m3u8`, `playlist.m3u8`, `manifest.m3u8`, `index.m3u8`) instead of redirect chains or single-bitrate links.
- If the origin requires request context, include the needed HTTP headers (commonly `http-user-agent` and/or `http-referrer`).
- Prefer “main” endpoints/redirectors that perform load-balancing, rather than hard-coding a single backend host.

Example (headers + adaptive):
```m3u
#EXTINF:-1 tvg-id="Example",Example Channel (720p)
#EXTVLCOPT:http-user-agent=Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0
#EXTVLCOPT:http-referrer=https://www.example.com/
https://edge.example.net/livecast/ik:example/manifest.m3u8
```

This reduces playback failures caused by redirects, missing headers, or non-load-balanced direct hosts.