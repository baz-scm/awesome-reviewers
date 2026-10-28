---
title: Cache keys and invalidation
description: 'A cache is only as correct as the key it is stored under and the triggers
  that evict it. Before adding a cache, enumerate every input that can change the
  cached value and either fold it into the key or wire an explicit invalidation:'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70976
---

A cache is only as correct as the key it is stored under and the triggers that evict it. Before adding a cache, enumerate every input that can change the cached value and either fold it into the key or wire an explicit invalidation:

1. **Key by everything that affects the result, not just an identifier.** A pinned-read cache keyed only by pin id kept serving results for an edited or removed tool call; it had to be keyed by the tool+arguments actually run. A plugin-tool inspection cache keyed only by file fingerprints missed a plugin being turned on/off at runtime; it needed the registry `state`/`updatedAt` and execution mode in the key too. A per-workspace service cache must be keyed by the *same* resolved path the rest of the app uses, not whatever `cwd` happens to be at process start.

```ts
// Bad: key omits inputs that change the value
cache.get(pin.id)

// Good: key captures everything the result depends on
const key = hash({ tool: pin.tool, args: pin.arguments, revision: pin.revision });
cache.get(key)
```

2. **Invalidate explicitly when a dependency changes.** If a setting or toggle controls what a cache contains (e.g. enabling cloud sessions changes what task history enumerates), the handler that changes the setting must call the cache's invalidation hook before the new state is read, rather than waiting for a TTL or relying on an unrelated code path to notice.

3. **For externally-mutable background data, use TTL with stale-while-revalidate, not a hard "forever" or "block until fresh" cache.** Return the cached value immediately so the UI doesn't flicker, kick off a background refresh once the entry ages past its TTL, and let an explicit user-triggered refresh bypass the TTL. Pick the TTL to match how fast the underlying data realistically changes.

4. **Give cached resources a bounded lifetime and a real dispose path.** Enforce size/byte budgets correctly (classify every variant of the data being measured, e.g. both `mediaType` and MCP's `mimeType` image blocks), evict on a clear LRU/idle policy, and avoid rewriting content that is already cached. Any cache backed by disk or other external storage needs a cleanup/dispose step — "write once at completion, never rewrite on later reads" beats "shorten and persist on every request" and prevents unbounded growth.

Treat cache-key completeness and invalidation triggers as part of design review for any new cache: if you can't name every input and every event that should clear or refresh an entry, the cache isn't ready to land.