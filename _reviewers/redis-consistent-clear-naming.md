---
title: Consistent Clear Naming
description: 'Use naming that is (1) safe per language rules, (2) semantically explicit,
  and (3) consistent with existing symbol families.


  Practical checklist:

  - Avoid reserved/unsafe identifier patterns. In C/C++, don’t introduce names starting
  with `_[A-Z]` (rename instead).'
repository: redis/redis
label: Naming Conventions
language: Other
comments_count: 5
repository_stars: 74261
---

Use naming that is (1) safe per language rules, (2) semantically explicit, and (3) consistent with existing symbol families.

Practical checklist:
- Avoid reserved/unsafe identifier patterns. In C/C++, don’t introduce names starting with `_[A-Z]` (rename instead).
- Make intent clear in the identifier. If a field like `check_time` can represent multiple checks, use a precise prefix that states what it tracks (e.g., `last_cron_check_time`, `client_last_cron_check_time`, etc.).
- Keep related APIs/handlers/constants consistent with the project’s naming “families.” If you already have `scanHashTable`, `scanListpack`, then a new counterpart should follow the same `scan*` pattern (e.g., `scanIntSet` when applicable). For cluster constants, align names with the established `CLUSTER_*` scheme (e.g., rename `GETSLOT_CROSSSLOT` → `CLUSTER_CROSSSLOT`).

Example:
```c
// Bad: reserved pattern in C11
REDISMODULE_API void (*_RedisModule_FreeString)(RedisModuleCtx *ctx, RedisModuleString *str);

// Good: renamed to a non-reserved identifier
REDISMODULE_API void (*RedisModule_FreeString_raw)(RedisModuleCtx *ctx, RedisModuleString *str);

// Good: semantic clarity via explicit prefix
// struct client { mstime_t last_cron_check_time; }

// Good: naming family consistency
void scanIntSet(client *c, robj *o, scanOptions *opts);

// Good: cluster constant consistency
#define CLUSTER_CROSSSLOT  (-2)
```