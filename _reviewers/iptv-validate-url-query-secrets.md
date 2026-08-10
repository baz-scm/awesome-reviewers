---
title: Validate URL Query Secrets
description: 'When accepting user-provided stream URLs, treat them as security-sensitive
  input: parse the URL and reject links that appear to contain expiring-session credentials
  or secrets in the query string. These are typically short/unsigned tokens, hashes,
  or random identifiers (e.g., nimblesessionid, authid, key, secret, hmac, token,
  e, ip, st). Such URLs are...'
repository: iptv-org/iptv
label: Security
language: Markdown
comments_count: 1
repository_stars: 135586
---

When accepting user-provided stream URLs, treat them as security-sensitive input: parse the URL and reject links that appear to contain expiring-session credentials or secrets in the query string. These are typically short/unsigned tokens, hashes, or random identifiers (e.g., nimblesessionid, authid, key, secret, hmac, token, e, ip, st). Such URLs are usually session-protected, temporary, and can leak sensitive parameters.

Practical standard:
- Require the link to be a direct media/broadcast endpoint (e.g., m3u8/mpd, UDP, RTMP, direct playlist/play URLs).
- Parse query parameters; if any “credential-like” parameter exists, reject.
- In particular, reject URLs where query values look like random/hash values (long alphanumeric, base64-like, or numeric timestamps) paired with keys such as: token, hmac, st, secret, authid, key, nimblesessionid, ip, e.
- If the provider enforces access via user-agent/referer/geo, require contributors to explicitly document it; do not accept authorization/IP-restricted streams.

Example (reject):
- https://example.com/live?stream=chan&nimblesessionid=21683442
- https://example.com/play?token=XYZ...&hmac=abc...&st=Lz1QtjfblUmkawUbk1Mx6w
- https://example.com/stream?ip=10.0.0.1&secret=f8z1l7gk

Example (accept):
- https://cdn.domain.com/path/channel.m3u8
- https://cdn.domain.com/live?stream=channelname
- rtmp://10.0.0.1/prefix/channel