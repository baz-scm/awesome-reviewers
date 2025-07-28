---
title: Initialize before dereferencing
description: Always ensure buffers, containers, and data structures are properly initialized
  before passing them to functions that will dereference them. This prevents null
  pointer dereferences and undefined behavior.
repository: neovim/neovim
label: Null Handling
language: C
comments_count: 4
repository_stars: 91433
---

Always ensure buffers, containers, and data structures are properly initialized before passing them to functions that will dereference them. This prevents null pointer dereferences and undefined behavior.

Key practices:
1. **Initialize buffers before use**: When using dynamic containers like kvec, ensure they are properly sized before passing to functions that access their contents
2. **Use null safety annotations**: Apply `FUNC_ATTR_NONNULL_ALL` and similar attributes to function parameters that must not be null
3. **Make precise assertions**: Use specific assertions like `assert(argc > 0)` rather than `assert(argc >= 0)` when zero values are not valid
4. **Handle potentially null returns**: When calling functions like `os_getenv()` that can return null, check the result before dereferencing

Example from the codebase:
```c
// Before: Potential null dereference
if (swap_exists_action != SEA_NONE) {
  choice = (sea_choice_T)do_dialog(VIM_WARNING, _("VIM - ATTENTION"), msg.items, ...);
}

// After: Ensure buffer is initialized
kv_resize(*msg, IOSIZE);  // Initialize buffer before use
if (swap_exists_action != SEA_NONE) {
  choice = (sea_choice_T)do_dialog(VIM_WARNING, _("VIM - ATTENTION"), msg.items, ...);
}
```

This approach prevents static analysis tools from flagging potential null dereferences and ensures runtime safety by establishing clear contracts about what data must be valid before use.