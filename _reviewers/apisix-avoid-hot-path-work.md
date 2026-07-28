---
title: Avoid Hot-Path Work
description: 'When optimizing performance, ensure hot paths do only the minimum required
  work and never block while holding scarce resources. Apply these rules:


  - Gate expensive resolution/processing behind cheap checks (e.g., only resolve secrets
  if references exist; only buffer/scan when blocking is requested).'
repository: apache/apisix
label: Performance Optimization
language: Other
comments_count: 6
repository_stars: 16922
---

When optimizing performance, ensure hot paths do only the minimum required work and never block while holding scarce resources. Apply these rules:

- Gate expensive resolution/processing behind cheap checks (e.g., only resolve secrets if references exist; only buffer/scan when blocking is requested).
- Don’t hold pooled connections (Redis, DB, etc.) across outbound network calls; release/re-acquire around blocking operations.
- Memoize configuration-derived decisions and reuse prepared objects/parsers; avoid recomputing defaults and deep-copying large structures per request.
- Preserve fast paths by scoping changes to the exact feature flags/conditions; avoid broad behavior changes that remove optimizations.
- Avoid “fetch everything” background patterns; query/cache only the entities actually in use.

Example (secret gating + pooled Redis around outbound call):
```lua
-- Guard per-request deep work
if secret.has_secret_ref(upstream_ssl) then
    local resolved = apisix_secret.fetch_secrets(upstream_ssl, true)
    upstream_ssl = resolved
end

-- Release pooled Redis before outbound embedding request
local res = red:get(key)
if miss then
    local embedding = do_outbound_http_request(body) -- no Redis held
    -- re-acquire only for Redis writes/search
    -- e.g., ensure_index/knn_search using a fresh/checked-out connection
end
```

Use lightweight checks + memoization to keep latency stable under load, and structure code so scarce pools aren’t drained by long waits.