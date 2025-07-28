---
title: avoid Lua ternary traps
description: Avoid using the `condition and expr1 or expr2` pattern when `expr1` can
  be `nil` or `false`, as this will always return `expr2` regardless of the condition
  result. This is a common source of subtle bugs in Lua code.
repository: neovim/neovim
label: Null Handling
language: Other
comments_count: 2
repository_stars: 91433
---

Avoid using the `condition and expr1 or expr2` pattern when `expr1` can be `nil` or `false`, as this will always return `expr2` regardless of the condition result. This is a common source of subtle bugs in Lua code.

The pattern `condition and expr1 or expr2` only works correctly when `expr1` is guaranteed to be truthy. When `expr1` can be `nil` or `false`, the `or expr2` part will always execute, making the condition meaningless.

**Problematic examples:**
```lua
-- This will always return `enable`, never `nil`
vim.b[bufnr][var] = enable == vim.g[var] and nil or enable

-- This fails when enable is false
bufstate.enabled = enable ~= globalstate.enabled and enable or nil
```

**Safe alternatives:**
```lua
-- Use explicit if-else
if enable == vim.g[var] then
  vim.b[bufnr][var] = nil
else
  vim.b[bufnr][var] = enable
end

-- Use vim.F.if_nil for nil-specific cases
result = vim.F.if_nil(potentially_nil_value, fallback)
```

This pattern is particularly dangerous because it appears to work correctly in many cases, making the bug difficult to detect during testing.