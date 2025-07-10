---
title: Prefer early returns
description: When a function can determine an early result based on input validation
  or special cases, return immediately rather than assigning to a temporary variable
  and having a single exit point. Early returns reduce nesting, improve readability,
  and often result in more efficient code by making guard conditions more visible.
repository: torvalds/linux
label: Code Style
language: C
comments_count: 2
repository_stars: 197350
---

When a function can determine an early result based on input validation or special cases, return immediately rather than assigning to a temporary variable and having a single exit point. Early returns reduce nesting, improve readability, and often result in more efficient code by making guard conditions more visible.

```c
// Recommended:
static int convert_prio(const int prio)
{
    if (prio == CPUPRI_INVALID)
        return CPUPRI_INVALID;
    
    // Continue with normal processing
    return prio - 40;
}

// Avoid:
static int convert_prio(int prio)
{
    int cpupri;

    if (prio == CPUPRI_INVALID)
        cpupri = CPUPRI_INVALID;
    else
        cpupri = prio - 40;
        
    return cpupri;
}
```

Early validation helps prevent unnecessary operations when preconditions aren't met, and results in flatter code that's easier to understand and maintain. Using `const` for parameters that won't be modified also improves code clarity and can help the compiler optimize.