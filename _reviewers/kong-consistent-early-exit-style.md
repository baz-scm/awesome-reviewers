---
title: Consistent Early-Exit Style
description: 'When updating/adding code, prioritize readability and predictable control-flow:


  - Use early exits (return/goto/continue) for error/invalid states to avoid deep
  nesting/extra indentation.'
repository: Kong/kong
label: Code Style
language: Other
comments_count: 6
repository_stars: 43871
---

When updating/adding code, prioritize readability and predictable control-flow:

- Use early exits (return/goto/continue) for error/invalid states to avoid deep nesting/extra indentation.
- Keep error-handling visually tight (no distracting blank lines between the call and the error check).
- For error logs, follow formatting rules:
  - Avoid Lua string concatenation inside ngx_log/ngx.log; pass multiple arguments instead.
  - Use the required capitalization for error messages (e.g., don’t capitalize the message text).
- Prefer clearer positive conditions over negated/complex expressions, and simplify large if/else chains where possible.

Example pattern (body parsing + early exit + logging):
```lua
local body, err = kong.request.get_body()
if err then
  ngx_log(ngx.ERR, "cannot process request body: ", tostring(err))
  return
end

local identifier = body  -- proceed normally
```

Example logging without concatenation:
```lua
ngx_log(ngx.ERR, "request failed (", req_url, "): ", err)
```