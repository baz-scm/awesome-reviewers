---
title: Conditional expensive operations
description: Only execute expensive operations when they are actually necessary. Avoid
  paying performance costs for functionality that may not be used or when conditions
  don't require the expensive computation.
repository: neovim/neovim
label: Performance Optimization
language: Other
comments_count: 4
repository_stars: 91433
---

Only execute expensive operations when they are actually necessary. Avoid paying performance costs for functionality that may not be used or when conditions don't require the expensive computation.

Key strategies:
- **Conditional execution**: Wrap expensive calls in conditions that check if the operation is needed
- **Lazy loading**: Defer expensive initialization until actually required  
- **Demand-based setup**: Only set up costly event handlers or processing when the feature is actively used

Examples:

```lua
-- Bad: Always pay the fs_stat cost
local stat = vim.uv.fs_stat(f)

-- Good: Only pay the cost when needed
if follow_param then
  local stat = vim.uv.fs_stat(f)
end

-- Bad: Eager loading causes performance hit
complete = vim.treesitter.language._complete,

-- Good: Lazy loading avoids eager initialization
complete = function(...) return vim.treesitter.language._complete(...) end,

-- Bad: Everyone pays the cost regardless of usage
vim.api.nvim_create_autocmd('DiagnosticChanged', {
  callback = function() -- expensive string formatting end
})

-- Good: Only setup when default statusline is used
if using_default_statusline then
  vim.api.nvim_create_autocmd('DiagnosticChanged', {
    callback = function() -- expensive string formatting end
  })
end
```

This approach prevents unnecessary performance overhead by ensuring expensive operations are only executed when their results will actually be used or when the conditions genuinely require them.