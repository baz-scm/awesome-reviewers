---
title: Complete cache invalidation keys
description: 'A cache is only as correct as its invalidation logic, and the recurring
  failure mode across these reviews is a cache key or dirtiness check that omits some
  dimension the cached value actually depends on. Examples seen repeatedly: a history-search
  cache keyed on directory identity but not on rows written by another connection;
  an embedding cache invalidated...'
repository: can1357/oh-my-pi
label: Caching
language: TypeScript
comments_count: 21
repository_stars: 37317
---

A cache is only as correct as its invalidation logic, and the recurring failure mode across these reviews is a cache key or dirtiness check that omits some dimension the cached value actually depends on. Examples seen repeatedly: a history-search cache keyed on directory identity but not on rows written by another connection; an embedding cache invalidated via `PRAGMA data_version`, which never changes for commits on the same connection, so deletions were never evicted; a session-entry serialization cache that snapshotted fields "by identity" and missed in-place nested mutations, inherited/non-enumerable properties, accessors, `toJSON` hooks, and proxy-backed values — each one a separate round of bugs; a memory-instructions cache keyed on session file but not on the active branch, so branch navigation served a stale snapshot; a worker pool cache keyed on environment variables but initially missing the resolved working directory; a prompt-cache key that diverged between two call sites that should have shared a cache shard; and a UI item cache that wasn't keyed on the active theme.

Before caching a derived value, enumerate every input the computation actually reads — including nested object graphs (not just top-level identity), external writers, environment/working-directory state, and any selector like branch, scope, theme, or session that affects the result — and make the invalidation check (or cache key) a function of all of them. Prefer a single authoritative validity check (e.g., a value stamp, version counter, or structural comparison) derived mechanically from the inputs, over scattering manual "invalidate here" calls through the codebase; manual invalidation sites are easy to miss as new mutation paths are added, whereas a correctness-by-construction check (such as comparing the cache key with the current effective key, or deep-comparing the value that was actually read) cannot drift out of sync. When a cached computation can observe something that cannot be cheaply or safely re-checked (a stateful getter, a `toJSON` hook, a proxy), treat that case as "not cacheable" and recompute rather than risk serving stale output. Finally, document and test the invalidation boundary explicitly — add a regression test that mutates exactly the input the cache might miss (a nested field, a branch switch, a theme change, an external writer) and asserts the cache is not reused.

```ts
// Bad: shallow identity snapshot misses nested in-place mutation
function cached(entry) {
  if (cache.has(entry) && cache.get(entry).fields === entry.fields) {
    return cache.get(entry).line; // stale if entry.fields.foo.bar changed in place
  }
  ...
}

// Good: key/validate on every dimension the computation reads
function cached(entry) {
  const stamp = deepValueStamp(entry); // walks the actual graph read by the projector
  const hit = cache.get(entry);
  if (hit && hit.version === currentVersion(entry) && stampMatches(hit.stamp, stamp)) {
    return hit.line;
  }
  return recompute(entry);
}
```