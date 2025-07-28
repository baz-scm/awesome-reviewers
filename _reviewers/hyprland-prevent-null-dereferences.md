---
title: prevent null dereferences
description: Always verify pointers are valid before dereferencing to prevent crashes
  and undefined behavior. This applies to regular pointers, weak pointers, and return
  values from C functions that may return null.
repository: hyprwm/Hyprland
label: Null Handling
language: C++
comments_count: 7
repository_stars: 28863
---

Always verify pointers are valid before dereferencing to prevent crashes and undefined behavior. This applies to regular pointers, weak pointers, and return values from C functions that may return null.

Use implicit bool conversion instead of explicit null comparisons for cleaner code:
```cpp
// Preferred
if (ptr) {
    ptr->doSomething();
}

// Avoid
if (ptr != nullptr) {
    ptr->doSomething();
}
```

For weak pointers, use the appropriate check method:
- Use `operator bool` or `.expired()` when you only need to test validity
- Use `.lock()` only when you need the actual shared pointer

Apply guard patterns with early returns to reduce nesting:
```cpp
if (!ptr)
    return;
    
ptr->doSomething();
```

Pay special attention to C function returns that may be null:
```cpp
const char* env = getenv("VAR_NAME");
if (!env)
    return defaultValue;
```

Critical areas requiring null checks include: pointer dereferences in event handlers, accessing monitor/window objects that may be destroyed, and any pointer obtained from external APIs or lookups.