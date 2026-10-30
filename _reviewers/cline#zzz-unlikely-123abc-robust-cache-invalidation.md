---
title: Robust cache invalidation
description: Caches must be invalidated on every event that can make them stale, and
  invalidation must never race with in-flight reads. Common bugs in this codebase
  came from caches that outlived the context they were scoped to (a model catalog
  cached across an org/personal switch), caches keyed too loosely to dedupe correctly
  (identical generated images rewritten to...
repository: cline/cline#zzz-unlikely-123abc
label: Caching
language: TSX
comments_count: 5
repository_stars: 71035
---

Caches must be invalidated on every event that can make them stale, and invalidation must never race with in-flight reads. Common bugs in this codebase came from caches that outlived the context they were scoped to (a model catalog cached across an org/personal switch), caches keyed too loosely to dedupe correctly (identical generated images rewritten to new temp files on every snapshot), and caches cleared too bluntly or too narrowly (closing a tab leaving its diff cached, or invalidating only when a shallow count-based signature changed, which misses a changed line that doesn't change the count).

When adding or touching a cache:
1. Identify every event that can invalidate an entry (context switch, resource close, new data snapshot) and clear/refresh it then — don't rely on a coarse proxy signal (like item counts) that can miss real changes; prefer treating any new snapshot as "may be stale" and re-validating.
2. Key caches by content identity (e.g., a hash of type+data) when you need to dedupe equivalent values, not just by a transient id, to avoid unbounded duplication of files/memory.
3. Guard against races: tag cache entries with a generation/version counter that bumps on invalidation, so a response for a stale read that completes after invalidation is discarded instead of overwriting fresher state.
4. Prefer stale-while-revalidate over clear-and-block: mark an entry `stale` and keep serving it while a background refetch runs, rather than deleting it outright — this avoids UI flicker/spinners on routine polling, while still guaranteeing an eventual refresh when nothing is already in flight.
5. Tie cache lifetime to resource lifetime — e.g., clear temp-file caches together with the directories they reference on exit.

Example pattern for safe invalidation with generation guarding:
```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
  }
}

async function read(key: string) {
  const generation = generationRef.current.get(key) ?? 0;
  const result = await fetchValue(key);
  if ((generationRef.current.get(key) ?? 0) !== generation) return; // stale, discard
  applyResult(key, result);
}
```
Always add a test that exercises the invalidation path under concurrency (e.g., an in-flight read racing a cache clear) to confirm the stale result is discarded and exactly one follow-up fetch happens.</description>
</invoke>
