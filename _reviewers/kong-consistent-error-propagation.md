---
title: Consistent Error Propagation
description: 'When handling failures, choose behavior intentionally: either propagate
  a real error in a consistent format, or gracefully degrade only for *explicitly
  non-error* cases (e.g., notifications, permission edge cases). Avoid masking, asserting,
  or continuing after validation/parsing fails.'
repository: Kong/kong
label: Error Handling
language: Other
comments_count: 11
repository_stars: 43871
---

When handling failures, choose behavior intentionally: either propagate a real error in a consistent format, or gracefully degrade only for *explicitly non-error* cases (e.g., notifications, permission edge cases). Avoid masking, asserting, or continuing after validation/parsing fails.

Apply:
- **Never silently continue after an invalid input parse/match.** If a header/path/config is invalid, either `return nil, err` (or an appropriate response) or explicitly default while logging.
- **Use consistent error return contracts:** prefer `return nil, err` for failure; avoid returning booleans where callers expect `nil, err`.
- **Don’t use `assert` for expected client/invalid-data scenarios.** Return an error response / `nil, err` instead, so failures become controlled.
- **If you must use `pcall` for environment/phase constraints, handle failures explicitly** (e.g., separate “pcall failed due to missing subsystem” from “real operational error”). Don’t let `pcall` collapse meaningful errors into success paths.
- **Match error handling to context** (HTTP vs stream/subsystem; notification vs request).

Example (Lua error contract + explicit fallback):
```lua
local function get_context(headers)
  local trace_id = headers["x-instana-t"]
  if not trace_id then return nil end

  local parsed = trace_id:match("^(%x+)")
  if not parsed then
    -- invalid input: don't proceed with raw value
    return nil, "x-instana-t header invalid"
  end

  return parsed
end

-- usage
local trace_id, err = get_context(ngx.req.get_headers())
if err then
  ngx_log(ngx.WARN, err)
  return nil  -- or propagate: return nil, err
end
```

Use logging only when it’s part of the chosen error-handling policy (e.g., non-fatal notification missing handler), and keep error strings consistently formatted (e.g., lowercase-leading).