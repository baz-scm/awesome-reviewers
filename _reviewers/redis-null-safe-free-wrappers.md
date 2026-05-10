---
title: Null-safe Free Wrappers
description: 'When a free/cleanup API may receive NULL (or an invalid handle), don’t
  rely on ad-hoc checks at call sites. Instead, define a NULL-safe wrapper/helper
  that:'
repository: redis/redis
label: Null Handling
language: Other
comments_count: 3
repository_stars: 74261
---

When a free/cleanup API may receive NULL (or an invalid handle), don’t rely on ad-hoc checks at call sites. Instead, define a NULL-safe wrapper/helper that:
- No-ops when the argument is NULL (mirrors `free(NULL)` semantics).
- Avoids double-evaluation (store the argument in a temporary).
- Preserves compile-time type checking (use a correctly typed temporary; avoid unnecessary casts).
- Is safe to use across versions when needed (e.g., macro wrapper vs direct symbol).
- Also guard cleanup operations (e.g., `close`) to run only when the handle was actually acquired.

Example pattern (C):
```c
/* NULL-safe wrapper: evaluates arg once, type-checked, no-op on NULL */
#define Module_FreeStringSafe(ctx, str) \
    do { \
        RedisModuleString *_ms = (str); \
        if (_ms) RedisModule_FreeString(ctx, _ms); \
    } while (0)
```
Example guard (Tcl):
```tcl
if {$fd ne {}} {
    catch {close $fd}
}
```
Apply this rule consistently to any code path that frees/finalizes memory or resources that might be absent due to conditional logic or partial failures.