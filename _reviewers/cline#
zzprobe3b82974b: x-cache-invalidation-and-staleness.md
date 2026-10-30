---
title: Cache invalidation and staleness
description: When caching fetched or derived data (model catalogs, generated files,
  file/diff contents), explicitly invalidate entries whenever the underlying context
  changes — account/org switch, external edits, tab close, or a successful mutation
  (commit, discard, etc.). Never let a cache silently outlive the context it was built
  for.
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Caching
language: TSX
comments_count: 7
repository_stars: 71067
---

When caching fetched or derived data (model catalogs, generated files, file/diff contents), explicitly invalidate entries whenever the underlying context changes — account/org switch, external edits, tab close, or a successful mutation (commit, discard, etc.). Never let a cache silently outlive the context it was built for.

Guard against race conditions between async fetches and invalidation: tag each cache entry with a generation/version counter that is bumped on invalidation, and have in-flight requests check their generation before writing results, discarding themselves if a newer generation has since been set. This prevents a slow or superseded response from overwriting fresher data.

Prefer marking entries "stale" and triggering a background refetch over clearing the cache outright: keep rendering the last-known value while refreshing, so the UI doesn't flash loading spinners on every poll, and avoid firing a duplicate refetch for a key that's already loading.

For caches that store derived artifacts keyed by content (e.g., generated images written to disk), key the cache by a hash of the content rather than by occurrence, so repeated materialization of identical data reuses the existing entry instead of duplicating it.

Example pattern:
```ts
const readGenerationRef = useRef(new Map<string, number>());

function invalidate(key: string) {
  readGenerationRef.current.set(key, (readGenerationRef.current.get(key) ?? 0) + 1);
}

async function read(key: string) {
  const generation = (readGenerationRef.current.get(key) ?? 0) + 1;
  readGenerationRef.current.set(key, generation);
  const result = await fetchData(key);
  if (readGenerationRef.current.get(key) !== generation) return; // superseded
  applyResult(key, result);
}
```
Apply this generation-check + explicit-invalidation pattern consistently to any cache (in-memory maps, on-disk temp files, request-level caches) to eliminate stale reads and duplicate writes.</description>
</invoke>
