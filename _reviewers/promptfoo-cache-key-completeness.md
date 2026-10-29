---
title: Cache key completeness
description: A cache (or in-flight request dedupe) key must encode every parameter
  that can change the response, and an entry must only be reused when it truly represents
  the same logical request. Before adding or reusing a key, enumerate all inputs that
  affect behavior — timeouts/deadlines, credentials or profile identity, session/trace/memory
  IDs, retrieval filters,...
repository: promptfoo/promptfoo
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 26565
---

A cache (or in-flight request dedupe) key must encode every parameter that can change the response, and an entry must only be reused when it truly represents the same logical request. Before adding or reusing a key, enumerate all inputs that affect behavior — timeouts/deadlines, credentials or profile identity, session/trace/memory IDs, retrieval filters, abort scope — and include them in the key, or explicitly bypass caching/dedupe when they're present. Two callers with different timeouts (e.g. `1000` vs `"1e3"`) must not share one in-flight transport unless the timeout is part of the key:

```ts
// Bad: timeout not part of the key — different deadlines collide
const inflightCacheKey = getAbortSignalScopedKey(cacheKey, signal);

// Good: deadline is part of the sharing contract
const inflightCacheKey = `${timeout}:${getAbortSignalScopedKey(cacheKey, signal)}`;
```

Likewise, requests carrying volatile or sensitive per-call state (trace flags, session IDs, memory IDs, return-control results) must skip the cache entirely rather than risk leaking one caller's session data into another's cached response. Only persist successful, complete results — never cache an error response or a partial/streaming failure, since replaying it would turn a transient error into a permanent one. When an operation's cache boundaries (authorization scope, pagination, replay semantics) aren't fully defined, prefer not caching at all over shipping an incomplete cache. Finally, treat in-flight deduplication the same way: requests scoped to different `AbortSignal`s are logically different callers and must not share one underlying request, and any cache read/write that honors an abort signal must check for already-aborted signals up front and remove its listeners on completion to avoid leaks.