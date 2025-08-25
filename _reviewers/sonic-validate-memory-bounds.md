---
title: validate memory bounds
description: Always validate array and string bounds before accessing memory to prevent
  out-of-bounds access and potential crashes. When working with strings or arrays,
  especially those with known length information, check indices against the actual
  length before dereferencing pointers.
repository: bytedance/sonic
label: Null Handling
language: C
comments_count: 7
repository_stars: 8532
---

Always validate array and string bounds before accessing memory to prevent out-of-bounds access and potential crashes. When working with strings or arrays, especially those with known length information, check indices against the actual length before dereferencing pointers.

Key practices:
- Use available length information (like GoString.len) instead of relying on null terminators
- Check array indices against length before access
- Validate pointer bounds in loops and string operations

Example from the codebase:
```c
// Before accessing pos[i], always check bounds
if (i >= src->len) {
    return ERR_INVAL;  // Handle out-of-bounds case
}

// In string comparison, use length-bounded operations
static int _strcmp(const char *p, const char *q, size_t max_len) {
    size_t i = 0;
    while (i < max_len && *p && *q && *p == *q) {
        p++; q++; i++;
    }
    // Safe comparison within bounds
}
```

This prevents accessing invalid memory addresses that could lead to undefined behavior, crashes, or security vulnerabilities.