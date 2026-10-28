---
title: Safe cache invalidation
description: 'Caches must be invalidated exactly when the underlying data changes,
  and async population must be protected against races with invalidation.


  - Tie invalidation to concrete mutation events (download/delete/upload, switching
  context/org, etc.), not to time or incidental re-renders. For example, clear a cached
  catalog when the user switches account context so...'
repository: cline/cline#;sleep 4;
label: Caching
language: TSX
comments_count: 5
repository_stars: 70976
---

Caches must be invalidated exactly when the underlying data changes, and async population must be protected against races with invalidation.

- Tie invalidation to concrete mutation events (download/delete/upload, switching context/org, etc.), not to time or incidental re-renders. For example, clear a cached catalog when the user switches account context so the next read refetches fresh data, and clear a model-list cache when a pull or delete completes so the next picker open reflects reality.
- When multiple async reads/writes can race (e.g. a background snapshot refresh racing with an in-flight file read, or a stale response arriving after the cache entry was invalidated), guard with a generation/version counter per cache key. Bump the generation whenever an entry is dropped or marked stale, and discard any in-flight response whose generation no longer matches the current one instead of letting it clobber fresher data.
- Prefer marking entries `stale` and refetching only what's actively in use over blanket-clearing the whole cache; a hard clear can trigger redundant duplicate fetches for data nobody asked to refresh yet.
- For caches that materialize derived artifacts (e.g. writing base64 payloads to temp files), key by a content hash (type + data) rather than by call site/sequence, so repeated materialization of identical content reuses the existing artifact instead of duplicating it. Clean up hash-keyed caches together with their backing resources on shutdown.
- Add a regression test for each invalidation fix: simulate the race (e.g. hold a read open across a refresh/invalidation) and assert the final cached value is the fresh one and no duplicate work occurred.

Example pattern for generation-guarded reads:
```ts
const generationByKey = new Map<string, number>();

function invalidate(key: string) {
  generationByKey.set(key, (generationByKey.get(key) ?? 0) + 1);
}

async function read(key: string) {
  const generation = generationByKey.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generationByKey.get(key) ?? 0) !== generation) {
    return; // superseded while in flight; drop it
  }
  cache.set(key, result);
}
```