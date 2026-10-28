---
title: Cache invalidation and staleness
description: Caches that mirror external or mutable state (model catalogs, file contents,
  diffs, generated media) must have explicit, race-safe invalidation rather than relying
  on counts, timers, or "it'll refresh eventually."
repository: cline/cline;
label: Caching
language: TSX
comments_count: 5
repository_stars: 70964
---

Caches that mirror external or mutable state (model catalogs, file contents, diffs, generated media) must have explicit, race-safe invalidation rather than relying on counts, timers, or "it'll refresh eventually."

Apply these rules:
1. Invalidate on every known mutation point. Any action that can make a cached value stale (switching account/org, closing a tab, an external edit, a refresh button) must explicitly drop or mark stale the affected cache entries — do not assume a periodic refresh or a changed count will catch it. For example, switching from an org to a personal account must force the model catalog to be refetched rather than reusing the org's cached list.
2. Guard against out-of-order async responses with a generation/version token per cache key. Bump the generation whenever an entry is invalidated, and discard any in-flight response whose generation is stale when it resolves, so a slow read started before a refresh can't overwrite fresher data written after it:
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
  if ((readGenerationRef.current.get(key) ?? 0) !== generation) return; // superseded, drop it
  applyResult(key, result);
}
```
3. Invalidate all related keys together. If one logical entity has multiple cache entries (e.g., a file's content cache and its staged/worktree diff caches), closing or refreshing it must invalidate every associated key, not just the primary one, to avoid reopening into stale data.
4. Prefer marking entries stale-and-refetch over flushing them outright when a flicker-free UI matters: keep the previous value rendered while a fresh fetch is in flight, and swap in the new value only once it lands.
5. Key caches by content identity (e.g., a hash of type + data) rather than by occurrence, so repeated writes of identical data reuse the existing cache entry instead of accumulating duplicates.

Add a regression test for any invalidation fix: hold a read in flight, trigger the invalidating action, and assert the stale response is discarded and the fresh one wins.