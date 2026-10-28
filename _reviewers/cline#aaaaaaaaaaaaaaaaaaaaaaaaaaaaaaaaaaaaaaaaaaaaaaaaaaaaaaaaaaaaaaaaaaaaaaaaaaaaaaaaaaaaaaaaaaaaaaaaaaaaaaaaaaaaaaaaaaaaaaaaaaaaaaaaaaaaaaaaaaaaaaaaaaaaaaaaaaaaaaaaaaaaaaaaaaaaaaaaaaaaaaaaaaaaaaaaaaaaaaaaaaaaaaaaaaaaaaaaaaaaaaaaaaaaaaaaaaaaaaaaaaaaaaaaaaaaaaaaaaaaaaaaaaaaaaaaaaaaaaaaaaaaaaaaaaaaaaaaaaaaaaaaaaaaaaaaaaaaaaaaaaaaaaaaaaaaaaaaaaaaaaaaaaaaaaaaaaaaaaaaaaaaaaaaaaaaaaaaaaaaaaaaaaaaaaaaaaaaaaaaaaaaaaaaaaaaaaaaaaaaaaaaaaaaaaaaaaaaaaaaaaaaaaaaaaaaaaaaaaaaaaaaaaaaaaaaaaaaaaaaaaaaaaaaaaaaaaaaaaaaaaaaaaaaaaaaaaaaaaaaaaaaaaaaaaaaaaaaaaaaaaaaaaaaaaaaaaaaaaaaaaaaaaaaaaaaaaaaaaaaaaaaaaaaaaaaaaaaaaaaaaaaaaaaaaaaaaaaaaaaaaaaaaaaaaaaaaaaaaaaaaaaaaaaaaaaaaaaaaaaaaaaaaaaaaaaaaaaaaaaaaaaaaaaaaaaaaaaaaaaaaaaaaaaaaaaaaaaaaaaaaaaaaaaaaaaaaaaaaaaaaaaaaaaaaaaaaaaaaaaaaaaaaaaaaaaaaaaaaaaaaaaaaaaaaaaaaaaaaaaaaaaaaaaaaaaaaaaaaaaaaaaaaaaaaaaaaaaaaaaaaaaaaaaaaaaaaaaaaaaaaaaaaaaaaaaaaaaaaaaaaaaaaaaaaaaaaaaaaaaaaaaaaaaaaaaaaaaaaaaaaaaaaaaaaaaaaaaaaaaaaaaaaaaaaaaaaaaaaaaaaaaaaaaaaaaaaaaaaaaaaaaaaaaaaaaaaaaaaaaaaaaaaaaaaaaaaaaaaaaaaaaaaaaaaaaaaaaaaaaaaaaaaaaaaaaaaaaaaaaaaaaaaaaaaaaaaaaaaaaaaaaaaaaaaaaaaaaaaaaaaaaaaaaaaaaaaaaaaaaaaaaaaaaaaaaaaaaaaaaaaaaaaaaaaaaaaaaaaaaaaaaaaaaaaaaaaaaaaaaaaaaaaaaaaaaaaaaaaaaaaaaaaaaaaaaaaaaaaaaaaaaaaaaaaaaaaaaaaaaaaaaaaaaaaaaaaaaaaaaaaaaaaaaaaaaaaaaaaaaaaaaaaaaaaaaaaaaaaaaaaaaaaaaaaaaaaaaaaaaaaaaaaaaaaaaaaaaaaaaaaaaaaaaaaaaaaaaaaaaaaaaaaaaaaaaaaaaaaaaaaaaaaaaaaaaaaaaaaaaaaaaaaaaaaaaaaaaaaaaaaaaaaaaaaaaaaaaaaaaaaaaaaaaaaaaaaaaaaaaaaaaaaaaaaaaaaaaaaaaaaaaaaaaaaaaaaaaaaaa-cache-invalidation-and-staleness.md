---
title: Cache invalidation and staleness
description: When caching data (model catalogs, file/directory contents, git diffs,
  generated media, etc.), explicitly design for invalidation and for races between
  in-flight fetches and cache changes — don't just add a cache and assume it stays
  correct.
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Caching
language: TSX
comments_count: 6
repository_stars: 70965
---

When caching data (model catalogs, file/directory contents, git diffs, generated media, etc.), explicitly design for invalidation and for races between in-flight fetches and cache changes — don't just add a cache and assume it stays correct.

- Identify every event that makes a cached entry stale (switching account/org context, external file edits, closing a tab, a pull/delete/unload action, a new snapshot from polling) and invalidate or drop exactly the affected entries at that point, rather than relying on the cache to expire naturally. Example: refetch the model catalog each time a picker opens instead of reusing a cache computed under a different account.
- When a cache is refreshed or dropped, guard against async reads that were already in flight returning after the invalidation and overwriting fresher data. Use a per-key generation/version counter that is bumped whenever an entry is invalidated; when a pending read resolves, compare its captured generation against the current one and discard the result if it's stale. This avoids the common bug where a slow response "wins" over a newer snapshot.
```ts
const generations = new Map<string, number>();
function invalidate(key: string) {
  generations.set(key, (generations.get(key) ?? 0) + 1);
}
async function read(key: string) {
  const expected = generations.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generations.get(key) ?? 0) !== expected) return; // stale, drop it
  applyResult(key, result);
}
```
- Prefer marking entries "stale" (keep showing old data, re-read once) over wiping them outright when the underlying data likely still matches but might have changed slightly (e.g., counts match but content line changed) — this avoids flicker while still re-validating.
- For caches that materialize derived artifacts (e.g., writing files from base64 payloads), key the cache by a content hash/identity so repeated identical inputs reuse the same artifact instead of regenerating and leaking resources; clean up the cache alongside the artifacts it tracks.

Add a regression test for any fixed cache bug that exercises the race or invalidation path (e.g., hold a read open across a refresh/poll and assert the stale response doesn't clobber fresh data).