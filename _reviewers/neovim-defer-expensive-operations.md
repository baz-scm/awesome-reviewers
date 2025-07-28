---
title: defer expensive operations
description: Avoid performing expensive operations (like module loading, event emissions,
  or resource allocation) until they are actually needed. This pattern significantly
  improves startup time and runtime performance by reducing unnecessary work.
repository: neovim/neovim
label: Performance Optimization
language: Txt
comments_count: 2
repository_stars: 91433
---

Avoid performing expensive operations (like module loading, event emissions, or resource allocation) until they are actually needed. This pattern significantly improves startup time and runtime performance by reducing unnecessary work.

Key strategies:
- Move `require` calls from initialization code into the actual function implementations
- Remove or consolidate unnecessary events/operations that create overhead
- Defer resource-intensive setup until first use

Example of lazy require pattern:
```lua
-- Instead of eager loading at plugin initialization:
local foo = require("foo")
vim.api.nvim_create_user_command("MyCommand", function()
    foo.do_something()
end, {})

-- Defer the require until command execution:
vim.api.nvim_create_user_command("MyCommand", function()
    local foo = require("foo")  -- Load only when needed
    foo.do_something()
end, {})
```

This approach ensures that modules and their dependencies are only loaded when the functionality is actually used, rather than eagerly loading everything at startup. The same principle applies to other expensive operations like network calls, file I/O, or complex computations.