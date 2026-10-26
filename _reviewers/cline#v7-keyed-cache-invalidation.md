---
title: Keyed cache invalidation
description: 'When caching async data, prevent stale/in-flight responses from overwriting
  fresher cache entries, and only invalidate when inputs truly changed.


  **Standard**'
repository: cline/cline#v7
label: Caching
language: TSX
comments_count: 3
repository_stars: 70865
---

When caching async data, prevent stale/in-flight responses from overwriting fresher cache entries, and only invalidate when inputs truly changed.

**Standard**
1. **Invalidate caches per key with a generation/version.**
   - Maintain a `generationByKey` map.
   - When you drop/refresh a cache entry for `key`, increment that key’s generation.
   - Every request captures the generation at start; when it resolves, apply results only if the generation still matches.

2. **Use “stale” semantics for snapshot-driven updates (optional but recommended).**
   - If a snapshot marks data stale, keep showing the existing content but schedule/re-run exactly one follow-up read through the same generation/invalidation path.
   - Ensure manual refresh uses the same invalidation logic as automatic snapshot handling.

3. **Don’t reload caches on unrelated refresh triggers.**
   - Cache configuration that is stable for the process/app lifetime (e.g., app base URL) and resolve it once at startup.
   - Re-fetch only when the underlying inputs can change; otherwise avoid refresh-driven invalidation.

**Illustrative pattern (generation discard)**
```ts
const generationByKey = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    generationByKey.current.set(key, (generationByKey.current.get(key) ?? 0) + 1);
  }
}

async function readAndCache(key: string) {
  const gen = generationByKey.current.get(key) ?? 0;
  const result = await fetchDataForKey(key);

  // Only commit if this response is still current
  if ((generationByKey.current.get(key) ?? 0) !== gen) return;
  cache.set(key, result);
}
```

**Outcome**: predictable cache correctness under StrictMode/async races, fewer unnecessary reloads, and tests that assert late responses never replace newer data.