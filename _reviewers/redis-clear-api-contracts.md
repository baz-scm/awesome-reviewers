---
title: Clear API Contracts
description: Public APIs must make their guarantees and caller responsibilities explicit—especially
  around encapsulation, lifecycle/ownership, and callback semantics.
repository: redis/redis
label: API
language: Other
comments_count: 5
repository_stars: 74261
---

Public APIs must make their guarantees and caller responsibilities explicit—especially around encapsulation, lifecycle/ownership, and callback semantics.

Guidelines:
- Encapsulate internals: expose only what modules/users need; hide implementation details behind typedefs/opaque structs when appropriate.
- Define behavioral contracts in writing: if behavior depends on sentinels, ordering, or conditional invocation rules, document the exact meaning and required checks.
- Specify ownership and lifecycle for every callback/input/output:
  - Who owns input structs (e.g., is `conf` copied?) and what is the scope of that ownership?
  - For `out` parameters like `*meta`, state what the API expects modules to do (e.g., whether to keep vs replace, and how to update pointers).
  - Clarify when free/unlink/copy callbacks may be invoked and on which threads.
- Prefer typed, intention-revealing signatures over “generic hide-the-type” parameters when the concrete type is known.
- Avoid unnecessary API complexity: if a simpler call pattern is safer and sufficiently performant, prefer it—and document any non-obvious semantic details.

Example pattern (copy callback semantics):
```c
/* Copy callback: update *meta and return whether metadata is kept. */
static int KeyMetaCopyCallback(RedisModuleKeyOptCtx *ctx, uint64_t *meta) {
    REDISMODULE_NOT_USED(ctx);
    char *str = (char *)*meta;
    if (str) {
        char *new_str = strdup(str);
        *meta = (uint64_t)new_str; /* API contract: update out-param */
    }
    return 1; /* keep metadata */
}
```

If you introduce sentinel values or out-parameter replacement behavior, treat it as an API contract: make the sentinel meaning explicit, define when callbacks are skipped, and provide short examples in the docs or tests so module authors don’t guess.