---
title: Use appropriate logging levels
description: Reserve logging statements for their appropriate purposes and levels.
  Use debugging-level logs (`sd_debug`) for development-time diagnostic information,
  and only use standard printing functions (`sd_printf`) for critical user-facing
  messages or error conditions. Excessive or incorrectly leveled logging creates noise
  in production systems and can impact...
repository: deeplearning4j/deeplearning4j
label: Logging
language: C++
comments_count: 3
repository_stars: 14036
---

Reserve logging statements for their appropriate purposes and levels. Use debugging-level logs (`sd_debug`) for development-time diagnostic information, and only use standard printing functions (`sd_printf`) for critical user-facing messages or error conditions. Excessive or incorrectly leveled logging creates noise in production systems and can impact performance.

Bad example:
```cpp
// Inappropriate for normal operation flow
sd_printf("Setting input buffer %d\n", index);
sd_printf("Pushing variable\n", 0);
sd_printf("realdiv: Pre variables\n", 0);
```

Good example:
```cpp
// For diagnostic information during development
sd_debug("Setting input buffer %d\n", index);
sd_debug("Pushing variable\n");

// For error conditions that users need to see
if(ptr == nullptr)
    sd_printf("ERROR: Context pointer is null!\n");
```

Consistent logging practices improve code readability, aid in debugging, and prevent log pollution in production environments.