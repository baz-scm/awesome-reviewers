---
title: Canonical Stream Naming
description: 'When editing M3U `#EXTINF` metadata, treat `tvg-id` (and related fields)
  as a canonical identifier: it must be valid, correctly aligned with the displayed
  channel name, and consistent across variants.'
repository: iptv-org/iptv
label: Naming Conventions
language: Other
comments_count: 12
repository_stars: 135586
---

When editing M3U `#EXTINF` metadata, treat `tvg-id` (and related fields) as a canonical identifier: it must be valid, correctly aligned with the displayed channel name, and consistent across variants.

Apply these rules:
- **Match identity:** `tvg-id` must correspond to the same channel as the human-readable name; don’t use unrelated or “unknown” ids.
- **Match scope:** don’t use **city/local call signs** for streams that are **national** (and vice versa).
- **Use canonical spelling/format:** keep `tvg-id` stable across entries (e.g., don’t mix `MeTV+` naming into different id spellings).
- **Avoid invalid/malformed attributes:** keep `tvg-id` simple and well-formed; don’t invent extra, conflicting attributes.
- **Handle variants intentionally:** if a stream is truly an alternative/different feed, don’t reuse the same canonical `tvg-id` incorrectly—use the correct canonical id (or place it in the appropriate list).
- **Reflect known constraints consistently:** if a channel is geo-blocked, include the standardized tag (e.g., `[Geo-blocked]`) in the name.

Example (showing the intended shape):
```m3u
#EXTINF:-1 tvg-id="MeTVPlus.us",MeTV+ (720p)
https://example.com/metvplus/index.m3u8
```

If you can’t confirm the canonical `tvg-id` for the exact channel (or its scope), omit the entry’s misleading identifier or use the correct one rather than guessing.