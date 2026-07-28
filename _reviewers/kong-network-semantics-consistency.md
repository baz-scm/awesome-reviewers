---
title: Network semantics consistency
description: 'When implementing HTTP/TCP/WebSocket/networking logic, treat protocol
  semantics as “correctness-critical”: don’t rely on accidental behavior, and don’t
  assume inputs are single-valued.'
repository: Kong/kong
label: Networking
language: Other
comments_count: 7
repository_stars: 43871
---

When implementing HTTP/TCP/WebSocket/networking logic, treat protocol semantics as “correctness-critical”: don’t rely on accidental behavior, and don’t assume inputs are single-valued.

Apply these rules:
1) Be consistent about connection lifecycle
- If you use a higher-level HTTP client (e.g., lua-resty-http), assume it manages keepalive/SSL as documented; don’t partially override by mixing raw socket operations unless you fully own SSL/keepalive/close behavior.
- For correctness tests/connection reuse issues, prefer fully closing the underlying socket over half-close patterns.

2) Defensively handle multi-value headers
- In OpenResty, the same header name can yield a string or a table when the client sends duplicates. Pick a deterministic rule (e.g., “take first” or “ignore if duplicated”) and enforce it.

3) Normalize outbound URLs
- Ensure URL paths are absolute (e.g., prepend “/” when missing) before passing to request/builders.

4) Avoid fragile query parsing/merging
- Naive string parsing can drop duplicate keys and mishandle encoding/edge cases. If correct merging semantics are unclear, avoid merging or use a proper query parser that preserves duplicates.

5) Parse WebSocket subprotocol lists correctly
- For `Sec-WebSocket-Protocol`, treat it as a list of tokens and compare exact compatible values—don’t use substring matching.

Example (multi-value header handling):
```lua
local function first_header_value(v)
  if type(v) == "table" then
    return v[1]
  end
  return v
end

local instana_t = first_header_value(headers["x-instana-t"])
local instana_s = first_header_value(headers["x-instana-s"])
```