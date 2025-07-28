---
title: Follow established API patterns
description: APIs should follow documented conventions and established patterns within
  the codebase to ensure consistency and predictability. This includes adhering to
  naming conventions, parameter structures, and interface designs that users already
  expect.
repository: neovim/neovim
label: API
language: Txt
comments_count: 6
repository_stars: 91433
---

APIs should follow documented conventions and established patterns within the codebase to ensure consistency and predictability. This includes adhering to naming conventions, parameter structures, and interface designs that users already expect.

Key patterns to follow:
- Use `enable(boolean)` pattern instead of separate `start()` and `stop()` functions
- Prefer filter kwargs tables over multiple individual parameters for extensibility
- Follow documented patterns in `:help dev-patterns` and `:help dev-naming`
- Maintain consistency with existing similar APIs in the same domain

Example of inconsistent API:
```lua
-- Inconsistent - uses start/stop pattern
vim.lsp.on_type_formatting.start(bufnr, client_id)
vim.lsp.on_type_formatting.stop(bufnr, client_id)

-- Inconsistent - individual parameters
enable(enable, bufnr, client_id)
```

Example of consistent API following established patterns:
```lua
-- Consistent - follows enable(boolean) pattern like other LSP features
vim.lsp.on_type_formatting.enable(true, {bufnr = bufnr, client_id = client_id})

-- Consistent - uses filter kwargs like other APIs
vim.lsp.linked_editing_range.enable(true, {bufnr = bufnr, client_id = client_id})
```

This consistency reduces cognitive load for users who can predict API behavior based on established patterns, and makes the codebase easier to maintain by following uniform conventions.