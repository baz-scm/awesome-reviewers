---
title: avoid unnecessary configuration
description: Avoid creating special-purpose configuration options when simpler alternatives
  exist. Don't force users to call setup functions or provide explicit configuration
  for basic functionality to work.
repository: neovim/neovim
label: Configurations
language: Txt
comments_count: 4
repository_stars: 91433
---

Avoid creating special-purpose configuration options when simpler alternatives exist. Don't force users to call setup functions or provide explicit configuration for basic functionality to work.

As noted in the discussions: "special-purpose options are clumsy and a maintenance burden" and "users will be forced to call this function in order to use your plugin, even if they are happy with the default configuration."

Instead of creating configuration options, consider:
- Documenting event handlers that users can copy into their config
- Allowing plugins to work out of the box with smart defaults
- Separating configuration from initialization logic
- Using existing Vim mechanisms like autocommands or filetype detection

Example of what to avoid:
```lua
-- Don't force this pattern
vim.g.query_autoreload_on = { 'InsertLeave', 'TextChanged' }

-- Instead, document the underlying mechanism
vim.api.nvim_create_autocmd('BufWritePost', {
  pattern = '*.scm',
  callback = function() vim.treesitter.query.invalidate_cache() end
})
```

For operations that require user consent (like network downloads), provide confirmation prompts rather than configuration flags. This maintains security while avoiding configuration complexity.