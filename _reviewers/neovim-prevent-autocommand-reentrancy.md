---
title: prevent autocommand reentrancy
description: Guard against reentrancy issues when operations may trigger autocommands
  or async events that could invalidate state or cause recursive execution. Check
  for existing execution context before proceeding and validate that pointers/state
  remain valid after operations that may trigger autocommands.
repository: neovim/neovim
label: Concurrency
language: C
comments_count: 3
repository_stars: 91433
---

Guard against reentrancy issues when operations may trigger autocommands or async events that could invalidate state or cause recursive execution. Check for existing execution context before proceeding and validate that pointers/state remain valid after operations that may trigger autocommands.

Key practices:
1. **Check execution state early**: Before operations that may trigger autocommands, check if similar operations are already running and fail with clear error messages
2. **Validate state after autocommands**: After operations like `win_new_tabpage()` or `win_set_buf()`, verify that pointers and handles are still valid before using them
3. **Use proper event scheduling**: For operations that must be deferred, use mechanisms like `multiqueue_put()` to schedule on appropriate event loops rather than blocking

Example from the codebase:
```c
// Check for reentrancy before proceeding
if (in_filetype_autocmd()) {
    api_set_error(err, kErrorTypeException,
                  "Cannot detect default while FileType autocommands are running");
    return;
}

// After operations that trigger autocommands, validate state
tabpage_T *tp = win_new_tabpage(after, buf->b_ffname, enter);
if (!tp) {
    // tp may have been freed by autocommands
    api_set_error(err, kErrorTypeException, "Failed to create tabpage");
    return 0;
}
// Validate tp->tp_firstwin is still valid before using
```

This prevents race conditions where autocommands modify global state during API operations, leading to crashes or data corruption.