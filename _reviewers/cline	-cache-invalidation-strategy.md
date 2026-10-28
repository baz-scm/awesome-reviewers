---
title: Cache invalidation strategy
description: 'Caches must be invalidated explicitly whenever the data they represent
  can change, not inferred from fragile heuristics (e.g. comparing item counts, which
  misses same-count content changes). Tie invalidation to the actual event that stales
  the data: switching accounts/orgs, completing a download/delete, closing a tab,
  or receiving a fresh snapshot from the...'
repository: "cline/cline\t"
label: Caching
language: TSX
comments_count: 6
repository_stars: 70947
---

Caches must be invalidated explicitly whenever the data they represent can change, not inferred from fragile heuristics (e.g. comparing item counts, which misses same-count content changes). Tie invalidation to the actual event that stales the data: switching accounts/orgs, completing a download/delete, closing a tab, or receiving a fresh snapshot from the source of truth. When an event can make a cache stale, actively clear or mark the affected entries rather than hoping the next read happens to differ.

Guard against races between invalidation and in-flight reads: tag each cache entry/request with a generation or version counter that is bumped on invalidation, and discard any response whose generation is older than the current one so a slow stale fetch can never clobber fresher data. If a fetch for a key is already in flight when new data invalidates it, don't kick off a duplicate request — mark the entry stale and let the in-flight read's completion trigger exactly one follow-up fetch.

For user-facing data, prefer a stale-while-revalidate approach: keep rendering the previous cached value while a refresh runs in the background, instead of clearing the cache and showing a loading spinner, so periodic polling or refreshes don't cause visible flicker.

When caching derived artifacts (e.g. materialized files from hashes/content), key the cache by a content hash so identical inputs are deduplicated and reused instead of regenerating/rewriting, and clean up the cache together with any backing resources on shutdown.

Example pattern:
```ts
const generation = new Map<string, number>();

function invalidate(key: string) {
  generation.set(key, (generation.get(key) ?? 0) + 1);
  cache.set(key, { ...cache.get(key), stale: true });
}

async function read(key: string) {
  const gen = generation.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generation.get(key) ?? 0) !== gen) return; // stale response, discard
  cache.set(key, { ...result, stale: false });
}
```

Always add a test that exercises the race: hold a read in flight, invalidate the cache, and assert the stale response is discarded while exactly one fresh follow-up read occurs.