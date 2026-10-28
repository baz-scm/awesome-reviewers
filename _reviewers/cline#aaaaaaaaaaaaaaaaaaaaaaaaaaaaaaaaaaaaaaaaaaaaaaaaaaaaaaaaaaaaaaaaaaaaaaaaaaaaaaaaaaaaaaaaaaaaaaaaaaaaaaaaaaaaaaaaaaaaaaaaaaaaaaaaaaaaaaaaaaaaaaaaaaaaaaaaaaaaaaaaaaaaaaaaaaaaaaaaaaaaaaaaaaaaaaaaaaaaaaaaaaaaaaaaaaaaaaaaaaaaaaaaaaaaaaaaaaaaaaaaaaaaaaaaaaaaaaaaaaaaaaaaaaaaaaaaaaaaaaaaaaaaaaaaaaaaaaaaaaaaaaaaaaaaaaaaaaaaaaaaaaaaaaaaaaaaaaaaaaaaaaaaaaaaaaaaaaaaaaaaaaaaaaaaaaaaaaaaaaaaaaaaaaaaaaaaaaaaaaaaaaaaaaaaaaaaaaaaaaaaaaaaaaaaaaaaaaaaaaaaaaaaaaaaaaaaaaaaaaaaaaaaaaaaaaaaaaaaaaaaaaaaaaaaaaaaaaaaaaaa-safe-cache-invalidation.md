---
title: Safe cache invalidation
description: Caches must be invalidated by genuine state changes, not by proxy signals
  that can miss real updates. For example, comparing a derived "signature" (like counts
  of changed files) to decide staleness missed cases where content changed but counts
  stayed the same; switching to simply marking all cached entries stale on every new
  snapshot of the source-of-truth...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Caching
language: TSX
comments_count: 4
repository_stars: 70964
---

Caches must be invalidated by genuine state changes, not by proxy signals that can miss real updates. For example, comparing a derived "signature" (like counts of changed files) to decide staleness missed cases where content changed but counts stayed the same; switching to simply marking all cached entries stale on every new snapshot of the source-of-truth fixed this class of bug. Similarly, a model catalog cached per-session went stale when the user switched accounts/orgs because nothing forced a refetch — the fix was to always fetch fresh data on the relevant UI entry point and replace the cache wholesale.

When caching derived artifacts (e.g., materialized files from data), key the cache by content identity (a hash of the meaningful inputs) rather than by call site or sequence, so repeated identical work reuses the existing entry instead of duplicating it on disk or elsewhere. Always tie cleanup of such cache-backed resources to the cache's lifecycle (e.g., clear files when the cache entry is cleared/on process exit).

Prefer a stale-while-revalidate pattern for UI-facing caches: when underlying data changes, mark affected entries stale but keep rendering the previous value, then refetch in the background so the UI doesn't flash a loading state. Guard the refetch path with generation/version counters per cache key so that:
- a request already in flight for a key is not duplicated when a new staleness signal arrives — let it finish and issue one follow-up read if needed;
- a late response from a superseded request never overwrites fresher data.

Example pattern for generation-guarded refresh:
```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(key: string) {
  generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
}

async function refresh(key: string) {
  const generation = generationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generationRef.current.get(key) ?? 0) !== generation) return; // superseded, drop it
  applyResult(key, result);
}
```

Applying these rules — invalidate on real state changes, key by content, revalidate in the background, and guard against race conditions — prevents stale data, duplicate work, and UI flicker.