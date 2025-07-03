---
title: Use utility macros
description: Use predefined utility macros for common operations instead of repeating
  manual calculations throughout your code. This improves readability, consistency,
  and reduces the likelihood of errors in calculations.
repository: dotnet/runtime
label: Code Style
language: C
comments_count: 2
repository_stars: 16578
---

Use predefined utility macros for common operations instead of repeating manual calculations throughout your code. This improves readability, consistency, and reduces the likelihood of errors in calculations.

For example, instead of manually calculating array sizes:

```c
// Don't do this
if (wcsncmp(path, DevicePathPrefix, sizeof(DevicePathPrefix) / sizeof(WCHAR) - 1) == 0)
    return NULL;

// Do this instead
if (wcsncmp(path, DevicePathPrefix, STRING_SIZE(DevicePathPrefix) - 1) == 0)
    return NULL;
```

Check for existing utility macros in your project (such as `ARRAY_SIZE`, `STRING_SIZE` in util.h) before writing common calculations. This practice ensures consistent implementation across the codebase and makes future maintenance easier by centralizing any changes needed to these calculation patterns.
