---
title: reuse concurrency infrastructure
description: Avoid implementing custom concurrency patterns when existing infrastructure
  is available. Before creating new debouncing, async/await, or parallel execution
  code, check if suitable implementations already exist in the codebase.
repository: neovim/neovim
label: Concurrency
language: Other
comments_count: 3
repository_stars: 91433
---

Avoid implementing custom concurrency patterns when existing infrastructure is available. Before creating new debouncing, async/await, or parallel execution code, check if suitable implementations already exist in the codebase.

For example, instead of implementing a custom debounce function:

```lua
local function debunce(f, timeout)
  local timer = nil
  return function(...)
    local args = { ... }
    if timer then
      vim.uv.timer_stop(timer)
      timer:close()
      timer = nil
    end
    timer = assert(vim.uv.new_timer())
    vim.uv.timer_start(timer, timeout, 0, vim.schedule_wrap(function()
      if timer then
        vim.uv.timer_stop(timer)
        timer:close()
        timer = nil
      end
      f(unpack(args))
    end))
  end
end
```

Reuse existing debouncing infrastructure like `next_debounce` in `lsp/_changetracking.lua`. Similarly, prefer established async patterns like `vim.async.await(3, vim.system, cmd, opts)` over manual coroutine implementations.

This reduces code duplication, ensures consistent behavior across the codebase, and leverages battle-tested concurrency primitives that handle edge cases and performance optimizations.