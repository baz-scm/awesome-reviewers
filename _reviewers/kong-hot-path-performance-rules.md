---
title: Hot-Path Performance Rules
description: 'Default to performance-aware coding for hot paths (proxy routing, request
  parsing, metrics/serialization, and request body handling):


  - **Avoid unnecessary periodic work**: only schedule timers or run refresh logic
  when the correctness mode requires it.'
repository: Kong/kong
label: Performance Optimization
language: Other
comments_count: 9
repository_stars: 43871
---

Default to performance-aware coding for hot paths (proxy routing, request parsing, metrics/serialization, and request body handling):

- **Avoid unnecessary periodic work**: only schedule timers or run refresh logic when the correctness mode requires it.
- **Do not add extra O(n) work in hot paths**: avoid length/count scans like `tb_nkeys()` on request-critical structures; prefer constant-time checks (e.g., `next()`-based) or use existing router-provided capture counts.
- **Reuse per-module/per-conf objects**: never allocate metatables/functions/large helper tables inside request-handling functions when the structure is reusable.
- **Minimize nginx/Kong accessor overhead**: prefer the cheaper single-value accessors (`ngx.ctx`, `ngx.var.http_content_type`, `ngx.header[name]`) over higher-level helpers when the value is already available.
- **Eliminate redundant per-request work**: ensure request body reads happen only once per request lifecycle.
- **Guard expensive debug logging**: don’t build JSON/strings for debug logs unless debug logging is enabled.
- **Measure before simplifying**: if you propose a code simplification in a performance-sensitive utility, require a microbenchmark/profile result—simpler code can be slower.

Example (constant-time capture check + localizing `next`):
```lua
local next_ = next

-- captures = { [0]=full_path, [1]=cap1, ... }
local function has_uri_captured(captures)
  if not captures then return nil end
  -- constant-time check for any key other than [0]
  if captures[1] then
    return captures
  end
  return next_(captures, 0) and captures or nil
end
```

Example (reuse metatable outside the hot function):
```lua
local payload_mt = {
  __newindex = function(t, k, v)
    -- set dot-path values
  end,
}

local function build_payload(template_payload)
  return setmetatable(template_payload, payload_mt)
end
```

If you’re unsure whether a change is beneficial, treat it as a performance work item: profile/flamegraph or microbenchmark it under realistic inputs before merging.