---
title: Cache invalidation and staleness
description: Client-side caches (model catalogs, file contents, diffs, generated media)
  must be explicitly invalidated whenever the underlying data can change — on mutation
  (download, delete, write), on manual refresh, or when a fresh snapshot of the source
  arrives. Never let a cache persist past the point where it could return outdated
  data (e.g. a provider switch...
repository: cline/cline#$(sleep 4)
label: Caching
language: TSX
comments_count: 7
repository_stars: 70978
---

Client-side caches (model catalogs, file contents, diffs, generated media) must be explicitly invalidated whenever the underlying data can change — on mutation (download, delete, write), on manual refresh, or when a fresh snapshot of the source arrives. Never let a cache persist past the point where it could return outdated data (e.g. a provider switch hiding a model, or a deleted item still showing in a picker).

When invalidating:
- Prefer content- or key-based caching (e.g. hash of media type+data) so identical content is reused instead of duplicated, rather than blindly recreating entries on every read.
- Guard against race conditions from in-flight reads: tag each cache entry/read with a generation or version counter that is bumped on invalidation, and discard any response whose generation is stale so it cannot overwrite fresher data.
- Avoid UI flicker and redundant work: instead of clearing the cache outright, mark entries stale and keep showing the previous value while a single follow-up fetch runs in the background; don't trigger multiple overlapping refetches for the same entry if a read is already in flight.

Example pattern for safe invalidation with concurrent reads:
```ts
const generationRef = useRef(new Map<string, number>());
function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
  }
}

async function read(key: string) {
  const generation = generationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generationRef.current.get(key) ?? 0) !== generation) {
    return; // superseded by a newer invalidation; discard stale response
  }
  applyResult(key, result);
}
```
Add tests that hold a read in flight across an invalidation/refresh and assert the stale response is discarded while exactly one correct follow-up read lands.