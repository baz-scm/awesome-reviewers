---
title: Document non-obvious logic
description: Add clear comments explaining the purpose and reasoning behind complex
  or non-obvious code logic. Comments should explain 'why' certain implementation
  choices were made or how specific variables and conditions function, rather than
  just restating what the code does. This is especially important for security-related
  checks, timing mechanisms, interruption...
repository: dotnet/runtime
label: Documentation
language: C
comments_count: 2
repository_stars: 16578
---

Add clear comments explaining the purpose and reasoning behind complex or non-obvious code logic. Comments should explain 'why' certain implementation choices were made or how specific variables and conditions function, rather than just restating what the code does. This is especially important for security-related checks, timing mechanisms, interruption handling, and specialized attribute usage.

For example:
```c
/* Tracks the starting time of the wait loop to calculate the remaining timeout
 * when re-entering the loop after an interruption. */
DWORD start_ticks = GetTickCount();

// OR

/* Skip inlining methods requiring security objects to prevent
 * security context bypass vulnerabilities */
if (target_method->flags & METHOD_ATTRIBUTE_REQSECOBJ) {
    return FALSE;
}
```
