---
title: Cache invalidation and race safety
description: Caches must be explicitly invalidated whenever the underlying data can
  change outside the cache's own lifecycle (e.g. switching accounts/orgs, downloading
  or deleting a model, an external edit to a file, closing and reopening a view).
  Don't rely on re-renders or polling alone to pick up changes — clear or refresh
  the relevant cache entry at the exact point...
repository: cline/cline?foo=bar
label: Caching
language: TSX
comments_count: 6
repository_stars: 71082
---

Caches must be explicitly invalidated whenever the underlying data can change outside the cache's own lifecycle (e.g. switching accounts/orgs, downloading or deleting a model, an external edit to a file, closing and reopening a view). Don't rely on re-renders or polling alone to pick up changes — clear or refresh the relevant cache entry at the exact point the mutation happens.

When caching async reads, guard against race conditions between in-flight requests and invalidation: tag each cache entry with a per-key generation/version counter that is bumped whenever that entry is invalidated (refresh, close, external edit). When a response comes back, compare its captured generation to the current one and discard it if it's stale, so a slow in-flight read can never clobber fresher data. If an entry is marked stale while a read is already in flight, keep the current value visible, let that read land, and schedule exactly one follow-up fetch — don't eagerly clear and refetch, which causes flicker and duplicate requests.

Also prefer content-based cache keys (e.g. a hash of type+data) over always-fresh writes for derived/generated artifacts, so repeated identical inputs reuse the existing cache entry instead of duplicating expensive side effects (temp files, directories, network calls).

Example pattern for safe invalidation with in-flight reads:
```ts
const readGenerationRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    readGenerationRef.current.set(key, (readGenerationRef.current.get(key) ?? 0) + 1);
  }
}

async function read(key: string) {
  const generation = readGenerationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if (generation !== (readGenerationRef.current.get(key) ?? 0)) {
    return; // superseded by a later invalidation; discard
  }
  applyResult(key, result);
}
```

Apply this standard whenever introducing or modifying a cache: identify every place the underlying data can change, invalidate the cache there, and make sure in-flight reads can't overwrite data that was invalidated after they started.