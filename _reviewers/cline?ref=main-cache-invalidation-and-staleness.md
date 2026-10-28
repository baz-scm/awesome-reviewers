---
title: Cache invalidation and staleness
description: 'Caches must stay correct whenever the data they derive from can change
  out from under them. In particular: (1) When a cache''s scope depends on external
  context (account/org, selected provider, repo state), refetch and replace the cache
  on every context switch rather than relying on a possibly-wrong assumption that
  the cached value is still applicable — e.g....'
repository: cline/cline?ref=main
label: Caching
language: TSX
comments_count: 5
repository_stars: 70980
---

Caches must stay correct whenever the data they derive from can change out from under them. In particular: (1) When a cache's scope depends on external context (account/org, selected provider, repo state), refetch and replace the cache on every context switch rather than relying on a possibly-wrong assumption that the cached value is still applicable — e.g. a cloud model catalog cached for an org must be refreshed when the user switches to a personal account, not reused. (2) When caching derived artifacts for dedup/perf (e.g. materializing images to temp files), key the cache by a content hash so identical inputs reuse the existing entry instead of duplicating work/storage, and clean the cache up alongside any backing resources on teardown. (3) Any cache invalidation that is triggered by a user action (refresh, closing a tab, discarding a file) must also cancel or ignore in-flight reads for the same key; otherwise a stale response that resolves after the invalidation can silently overwrite fresher data. Guard against this with a per-key generation counter that is bumped on invalidation, and drop any response whose generation is no longer current:

```ts
const readGenerationRef = useRef(new Map<string, number>());
function invalidate(key: string) {
  readGenerationRef.current.set(key, (readGenerationRef.current.get(key) ?? 0) + 1);
}
async function read(key: string) {
  const generation = readGenerationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if ((readGenerationRef.current.get(key) ?? 0) !== generation) return; // stale, discard
  applyResult(key, result);
}
```

(4) Prefer marking cache entries "stale" and keeping the previous value rendered while a background refetch resolves, rather than clearing the cache outright — this avoids UI flicker (e.g. a spinner flashing on every poll) while still guaranteeing freshness once the refetch completes.</description>
