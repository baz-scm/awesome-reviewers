---
title: Cache invalidation discipline
description: Caches must be invalidated precisely when the data they hold could go
  stale, and keyed so identical content is reused instead of duplicated. When the
  underlying source of truth changes — switching account/org context, an explicit
  refresh, external file edits, or closing a tab/session — drop or refetch the corresponding
  cache entries rather than letting them...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Caching
language: TSX
comments_count: 4
repository_stars: 70986
---

Caches must be invalidated precisely when the data they hold could go stale, and keyed so identical content is reused instead of duplicated. When the underlying source of truth changes — switching account/org context, an explicit refresh, external file edits, or closing a tab/session — drop or refetch the corresponding cache entries rather than letting them linger indefinitely. For example, a cloud model catalog cached per-session went stale after switching organizations; the fix was to refetch on every open rather than reuse the cached list. Likewise, a file-contents/diff cache in a project panel needs to be cleared on manual refresh and have individual entries dropped when their tab closes, so reopening forces a fresh read instead of showing stale content.

When caching derived artifacts (e.g., materializing images to temp files), key the cache by a content hash rather than by occurrence, so repeated identical inputs reuse the existing artifact instead of creating duplicates that leak resources over time. Clean up these caches alongside their backing resources (e.g., temp directories) on shutdown.

Also guard against races between invalidation and in-flight reads: if a read was already in progress when the cache was invalidated, it must not overwrite the entry with stale data once it resolves. Use a per-key generation counter that's bumped on invalidation, and have in-flight operations check their captured generation before committing results to the cache — discarding the result if the generation has since moved on.

```ts
// bump generation on invalidation
function invalidate(key: string) {
  generations.set(key, (generations.get(key) ?? 0) + 1);
  cache.delete(key);
}

// in-flight read only commits if still current
async function read(key: string) {
  const generation = generations.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generations.get(key) ?? 0) !== generation) return; // stale, discard
  cache.set(key, result);
}
```