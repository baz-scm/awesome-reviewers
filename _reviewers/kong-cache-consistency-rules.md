---
title: Cache Consistency Rules
description: 'When implementing caching, make coherence and invalidation explicit
  and configuration-driven:


  - If a setting promises immediate consistency (e.g., “strict”), do not perform lazy
  reloads; rely on the update pipeline to keep cached data correct.'
repository: Kong/kong
label: Caching
language: Other
comments_count: 4
repository_stars: 43871
---

When implementing caching, make coherence and invalidation explicit and configuration-driven:

- If a setting promises immediate consistency (e.g., “strict”), do not perform lazy reloads; rely on the update pipeline to keep cached data correct.
- For multi-worker systems, prefer shared caches (e.g., ngx.shared or equivalent) so workers don’t recompute independently; unnecessary recomputation increases both CPU cost and inconsistency risk.
- Tie TTLs to the real invalidation mechanism. Don’t add TTL “just because” when cascade delete or another definitive mechanism already removes stale data. When a TTL is required, use the intended constant so behavior is predictable.

Example pattern (versioned + conditional reload):
```lua
-- cache state
local upstream_version = 0
local all_upstreams

local function reset_all_upstreams()
  -- recompute and repopulate shared/local state
  -- ...
  upstream_version = new_upstream_version
  all_upstreams = upstreams_dict
  return true
end

reload_all_upstreams = function()
  -- in strict consistency mode, skip reloads entirely
  if kong.configuration.upstream_consistency == "strict" then
    return true
  end

  -- otherwise reload only when upstreams changed
  if upstream_version == new_upstream_version then
    return true
  end

  return reset_all_upstreams()
end
```

Checklist to apply during review:
1) Does any config imply strict correctness? If yes, is lazy reload/invalidation disabled accordingly?
2) Is the cache shared across workers (or otherwise proven consistent)?
3) Is TTL aligned with how entries actually become invalid (TTL vs cascade delete vs explicit version updates)?