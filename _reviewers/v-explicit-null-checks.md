---
title: explicit null checks
description: Always verify that pointers and function return values are not null before
  dereferencing or using them. This prevents crashes and undefined behavior, especially
  when working with C functions or manual memory management.
repository: vlang/v
label: Null Handling
language: Other
comments_count: 4
repository_stars: 36582
---

Always verify that pointers and function return values are not null before dereferencing or using them. This prevents crashes and undefined behavior, especially when working with C functions or manual memory management.

Key practices:
- Check C function return values that can return null: `display := C.XOpenDisplay(0)` should be followed by a null check since XOpenDisplay is documented to return null on failure
- Assert pointer validity in tests: `assert green_arena.data != unsafe { nil }` and `assert green_arena.head != unsafe { nil }`
- Add defensive null checks in critical paths: `if g.fn_decl == unsafe { nil } || g.fn_decl.return_type == ast.void_type` prevents crashes when fn_decl might be uninitialized
- Set pointers to nil after freeing to make use-after-free bugs easier to detect: `current.next = unsafe { nil }` after `free(current)`

Example from discussions:
```v
// Bad: No null check for C function return
display := C.XOpenDisplay(0)
// Immediate use without verification

// Good: Check for null return
display := C.XOpenDisplay(0)
if display == unsafe { nil } {
    return error('Failed to open display')
}
defer { C.XCloseDisplay(display) }
```

This practice is essential for robust code that interfaces with C libraries or manages pointers manually.