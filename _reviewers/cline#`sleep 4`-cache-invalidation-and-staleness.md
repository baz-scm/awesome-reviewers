---
title: Cache invalidation and staleness
description: 'Caches must be tied to explicit invalidation events, and asynchronous
  reads must never let a stale result overwrite fresher data.


  - Invalidate or refresh a cache whenever the underlying source changes (e.g., switching
  accounts/orgs, installing/deleting a model, git status changes) rather than trusting
  a cache indefinitely. Prefer re-fetching fresh data at...'
repository: cline/cline#`sleep 4`
label: Caching
language: TSX
comments_count: 5
repository_stars: 70979
---

Caches must be tied to explicit invalidation events, and asynchronous reads must never let a stale result overwrite fresher data.

- Invalidate or refresh a cache whenever the underlying source changes (e.g., switching accounts/orgs, installing/deleting a model, git status changes) rather than trusting a cache indefinitely. Prefer re-fetching fresh data at the point of use (e.g., when a picker opens) or explicitly clearing the cache on the mutating action, instead of relying on time-based expiry alone.
- When caching derived artifacts from immutable content (e.g., materializing images/files from repeated data), key the cache by a content hash so repeated writes of identical data are deduped and reused instead of accumulating duplicate copies. Clean up these artifacts when the cache is cleared.
- Guard against race conditions between in-flight reads and cache invalidation. Use a generation/version counter per cache key that increments whenever that entry is invalidated; when an async read resolves, compare its captured generation to the current one and discard the result if it's stale instead of writing it into the cache. Avoid globally clearing an entire cache on refresh if only specific entries changed — mark affected entries individually (e.g., `stale: true`) so in-flight reads already in progress can still land, with one follow-up read scheduled afterward rather than restarting everything.

Example pattern:
```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(key: string) {
  generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
}

async function read(key: string) {
  const generation = generationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if (generation !== (generationRef.current.get(key) ?? 0)) {
    return; // stale result, a newer invalidation/read has superseded this one
  }
  cache.set(key, result);
}
```