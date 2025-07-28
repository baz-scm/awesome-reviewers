---
title: avoid error masking
description: Don't use mechanisms that suppress or hide errors unless absolutely necessary
  for the application flow. Error masking makes debugging difficult and can hide important
  issues from users and developers.
repository: neovim/neovim
label: Error Handling
language: Other
comments_count: 4
repository_stars: 91433
---

Don't use mechanisms that suppress or hide errors unless absolutely necessary for the application flow. Error masking makes debugging difficult and can hide important issues from users and developers.

**Problematic patterns to avoid:**
- Using `pcall()` just to ignore errors: "pcall masks errors"
- Adding `silent!` to commands unnecessarily: "silent with '!' silences errors..."
- Using fragile error checking like `vim.v.shell_error`

**Better alternatives:**
- Use `vim.schedule()` if you need to prevent errors from disrupting flow
- Use proper error handling utilities like `t.pcall_err` for testing
- Use `vim.system():wait()` instead of `vim.fn.system()` to avoid fragile error handling
- Let errors propagate naturally unless you have a specific reason to handle them

**Example:**
```lua
-- Bad: Masks the actual error
local ok, _ = pcall(api.nvim_command, 'edit')

-- Better: Use proper error handling utility
eq(':edit command in prompt buffer throws error',
   t.pcall_err(api.nvim_command, 'edit'))

-- Bad: Silences all errors
nvim_command('silent! edit `=__fname`')

-- Better: Let errors show unless specifically needed
nvim_command('edit `=__fname`')
```

Only suppress errors when you have a clear reason and a plan for handling the error condition appropriately.