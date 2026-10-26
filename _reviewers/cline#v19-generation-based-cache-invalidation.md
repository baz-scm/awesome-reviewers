---
title: Generation-Based Cache Invalidation
description: 'When caching async data per key (e.g., file contents, repo snapshots),
  prevent race conditions where late responses overwrite fresher cache entries.


  **Standard**'
repository: cline/cline#v19
label: Caching
language: TSX
comments_count: 3
repository_stars: 70885
---

When caching async data per key (e.g., file contents, repo snapshots), prevent race conditions where late responses overwrite fresher cache entries.

**Standard**
1. **Version every in-flight read per cache key** (generation/token).
2. **Invalidate by bumping the generation** when you drop/refresh the cache entry.
3. **Discard superseded responses** (or mark as stale and schedule a follow-up) so an old request can’t replace newer data.
4. **Test the race**: keep a read “in flight” across refresh/poll and assert the late response does not win.
5. **Only reload when source-of-truth can change**: don’t tie stable config (e.g., app base URL for the app lifetime) to unrelated refresh events.

**Pattern (React example)**
```ts
const genRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const k of keys) {
    genRef.current.set(k, (genRef.current.get(k) ?? 0) + 1);
  }
  // also clear/mark cache entries if needed
}

async function readKey(k: string) {
  const myGen = genRef.current.get(k) ?? 0;
  setCache(k, { loading: true });

  const data = await fetchSomethingForKey(k);

  // Ignore late responses
  if ((genRef.current.get(k) ?? 0) !== myGen) return;

  setCache(k, { data, loading: false });
}
```

Apply this to any per-path/per-file cache where refresh, tab switching, polling, or external edits can invalidate entries while requests are still in flight. For stable values whose backend/env won’t change during the app’s lifetime, resolve once and reuse rather than re-fetching on every account refresh/reconnect.