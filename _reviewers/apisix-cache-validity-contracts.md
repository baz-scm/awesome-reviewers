---
title: Cache Validity Contracts
description: 'When caching derived state, you must define (and encode) a validity
  contract: *what exact changes make the cached data incorrect*, and how that change
  is detected (keying and/or TTL/refresh).'
repository: apache/apisix
label: Caching
language: Other
comments_count: 8
repository_stars: 16922
---

When caching derived state, you must define (and encode) a validity contract: *what exact changes make the cached data incorrect*, and how that change is detected (keying and/or TTL/refresh).

Practical rules:
1) **Key caches on the right change marker**
   - Use config change indices such as `metadata.modifiedIndex` / `conf_version` as part of cache keys (so rebuild happens on metadata/config change, not only on LRU eviction or TTL).
2) **Include secret/external-data drift in validity**
   - If the cached output depends on secrets that don’t bump `conf_version`, bound staleness with a TTL/refresh or include a secret version in the validity check.
3) **Treat delete/empty updates as real changes**
   - In incremental caches, ensure delete events and “plugins becomes empty” updates still get recorded so the old cached entries are removed; don’t early-return before enqueueing reconciliation.
4) **Normalize entity identifiers across full vs incremental paths**
   - Any ID used to add/remove cached entries must be identical in both the incremental update path and the full rebuild path.
5) **Make cache-rebuild side effects idempotent**
   - If a cached object refreshes by recreating functions/closures, ensure repeated rebuild doesn’t stack wrappers (capture originals outside the per-build override, or guard with a one-time flag).

Code sketch (keying on a change marker):
```lua
-- Example pattern: include modifiedIndex in the cache key
local tracer, err = core.lrucache.plugin_ctx(
    lrucache,
    api_ctx,
    metadata.modifiedIndex, -- invalidates/rebuilds on metadata change
    create_tracer_obj,
    conf,
    plugin_info
)
```

Code sketch (don’t skip deletes/empty updates in incremental reconciliation):
```lua
local function filter(val)
  if not val.value then
    pending_delete = true
    has_pending = true
    -- record delete so reconciliation removes old entries
    return
  end
  -- ... even if val.value.plugins is empty, still record the update for reconciliation
end
```

Adhering to these rules prevents security/auth drift, stale behavior that only clears on TTL, and “rebuild-time” bugs caused by inconsistent IDs or non-idempotent refresh logic.