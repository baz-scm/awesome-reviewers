---
title: Generation-based cache invalidation
description: 'When you cache async data (files, diffs, remote lookups), prevent stale/late
  responses from overwriting newer cache state.


  **Standards**

  1. **Invalidate by key+generation (not by blind cache clearing).** Keep a `generation`
  per cache key. When you drop/refresh a cache entry, bump that key’s generation.'
repository: cline/cline#v14
label: Caching
language: TSX
comments_count: 3
repository_stars: 70876
---

When you cache async data (files, diffs, remote lookups), prevent stale/late responses from overwriting newer cache state.

**Standards**
1. **Invalidate by key+generation (not by blind cache clearing).** Keep a `generation` per cache key. When you drop/refresh a cache entry, bump that key’s generation.
2. **Discard superseded responses.** Each in-flight request captures the generation it started with; when it resolves, only apply results if the generation still matches.
3. **Handle “already loading” deterministically.** If a refresh/snapshot arrives while a read is in-flight:
   - either let the in-flight request complete but mark the entry `stale`, then
   - trigger **exactly one** follow-up read for that key after completion.
4. **Only refetch when dependencies change.** If the underlying inputs are fixed for the app/session lifetime (e.g., environment/config base URL), resolve once at startup and do not reload on unrelated refresh events.

**Example pattern (per-key generation + stale follow-up)**
```ts
const genRef = useRef(new Map<string, number>()); // key -> generation
const [cache, setCache] = useState(new Map<string, { stale?: boolean; value?: string }>());

function invalidate(keys: Iterable<string>) {
  for (const k of keys) genRef.current.set(k, (genRef.current.get(k) ?? 0) + 1);
  // Optionally mark as stale here rather than clearing everything.
}

async function readKey(key: string) {
  const startGen = genRef.current.get(key) ?? 0;
  setCache(c => new Map(c).set(key, { ...(c.get(key) ?? {}), stale: false }));

  const value = await fetchValueForKey(key);

  // Discard late responses
  if ((genRef.current.get(key) ?? 0) !== startGen) return;

  setCache(c => new Map(c).set(key, { ...c.get(key), value }));
}
```

Apply this consistently to eliminate “refresh then late response wins” bugs, and keep fetches aligned with the actual dependency changes (stable config should be fetched once, not on every refresh).