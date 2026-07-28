---
title: Nil-Safe Input Normalization
description: 'When handling optional/null values, normalize and guard them at the
  boundary so downstream code never has to guess.


  Apply these rules:

  1) Keep safe fallbacks for optional config fields (don’t delete “default” logic
  unless the field is strictly required).'
repository: Kong/kong
label: Null Handling
language: Other
comments_count: 10
repository_stars: 43871
---

When handling optional/null values, normalize and guard them at the boundary so downstream code never has to guess.

Apply these rules:
1) Keep safe fallbacks for optional config fields (don’t delete “default” logic unless the field is strictly required).
2) Normalize values to the expected type immediately:
   - If a header can be duplicated, `request.get_headers()[name]` may be a table; convert to the first string.
   - If an upstream value is sometimes nil/empty, treat empty as missing consistently.
3) Ensure string operations and serialization never receive `nil` (use nil checks/early returns, or set deterministic defaults).
4) Avoid producing arrays/lists with `nil` elements in the middle; either use deterministic defaults or filter out nils before iterating/serializing.
5) Add regression tests for shape differences (e.g., duplicate headers, missing route fields, nil-able config).

Example (normalize header values + nil-safe decode):
```lua
local function normalize_header(v)
  if type(v) == "table" then
    return v[1]
  end
  return v
end

local function get_first_valid_header(request_headers, name)
  return normalize_header(request_headers[name])
end

-- usage
local request_headers = request.get_headers()
local token_header = get_first_valid_header(request_headers, "authorization")
if type(token_header) ~= "string" or token_header == "" then
  return nil
end
```

Example (deterministic metric/tag element):
```lua
local route_name = message.route and message.route.name or ""
route_name = (route_name:gsub("%.", "_"))
-- always pass a string (or explicitly omit the element before building the array)
```