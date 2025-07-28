---
title: API consistency patterns
description: Ensure similar API functions use consistent parameter patterns, types,
  and behaviors. When designing new APIs or modifying existing ones, identify related
  functions and align their interfaces to create predictable, reusable patterns.
repository: neovim/neovim
label: API
language: Other
comments_count: 7
repository_stars: 91433
---

Ensure similar API functions use consistent parameter patterns, types, and behaviors. When designing new APIs or modifying existing ones, identify related functions and align their interfaces to create predictable, reusable patterns.

Key principles:
- Use consistent parameter types across similar functions (e.g., if one diagnostic function accepts `namespace` as number|table, others should too)
- Reuse common utility types and builders rather than creating function-specific ones
- Maintain consistent capability announcements across related LSP features
- Apply the same parameter validation and handling patterns to similar functions

Example from diagnostic APIs:
```lua
-- Inconsistent: some functions support table namespace, others don't
vim.diagnostic.get(bufnr, { namespace = {ns1, ns2} })  -- supported
vim.diagnostic.open_float(opts)  -- namespace as table not supported

-- Consistent: all diagnostic functions handle namespace parameter the same way
vim.diagnostic.get(bufnr, { namespace = ns_or_table })
vim.diagnostic.open_float({ namespace = ns_or_table })
```

This approach reduces cognitive load for users, enables code reuse, and makes the API more maintainable. Before implementing new functionality, survey existing similar APIs and adopt their established patterns rather than inventing new ones.