---
title: Stale-Cache Read Guard
description: When caching async data, ensure late or superseded responses cannot overwrite
  fresher cache state, and invalidate/reload entries using a consistent lifecycle.
repository: cline/cline#v1
label: Caching
language: TSX
comments_count: 3
repository_stars: 70862
---

When caching async data, ensure late or superseded responses cannot overwrite fresher cache state, and invalidate/reload entries using a consistent lifecycle.

Apply these rules:
1) Use per-cache-key generations/versions.
- Keep a read-generation counter per cache key/path.
- Increment (bump) the generation whenever you drop/refresh/invalidate that key.
- When an async read resolves, only apply it if its generation still matches.

2) Mark entries stale instead of blindly clearing.
- On snapshot/state changes, mark cached entries stale.
- If a read is already in flight, decide explicitly:
  - Either keep the in-flight response and schedule a single follow-up read if the entry was marked stale, or
  - Discard it if it was superseded by a newer generation.

3) Make refresh paths consistent.
- Route manual refresh through the same invalidation logic as automatic updates (don’t special-case by clearing caches in a different way).

4) Cache by correct lifecycle.
- Don’t re-fetch “startup-resolved” configuration on unrelated refreshes.
- Retry only when the initial lookup failed; otherwise keep the cached value across account refreshes/reconnects.

Example pattern (per-key generation):
```ts
const genByKey = new Map<string, number>();
const invalidate = (keys: Iterable<string>) => {
  for (const k of keys) genByKey.set(k, (genByKey.get(k) ?? 0) + 1);
};

async function readAndCache(key: string) {
  const gen = genByKey.get(key) ?? 0;
  const value = await fetchValue(key);
  if ((genByKey.get(key) ?? 0) !== gen) return; // discard stale
  cache.set(key, value);
}
```

This prevents stale async results from clobbering newer cache state and reduces unnecessary re-fetching, aligning caching behavior with both correctness and performance.