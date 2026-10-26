---
title: Async cache invalidation
description: 'When caching async results (per key/path/user/env), ensure correctness
  under concurrency and avoid needless reloads.


  **Rules**

  1. **Version/tag each cached read**: associate every in-flight fetch with a per-key
  “generation” (monotonic counter or version). Store the current generation when starting
  the request.'
repository: cline/cline#v5
label: Caching
language: TSX
comments_count: 2
repository_stars: 70864
---

When caching async results (per key/path/user/env), ensure correctness under concurrency and avoid needless reloads.

**Rules**
1. **Version/tag each cached read**: associate every in-flight fetch with a per-key “generation” (monotonic counter or version). Store the current generation when starting the request.
2. **Invalidate by bumping generation**: whenever you drop/refresh a cache entry (e.g., tab close, explicit refresh, content edited), increment/bump the generation for that key/path.
3. **Discard stale responses**: before writing fetched data into cache/state, verify the response generation matches the latest generation. If not, ignore it.
4. **Only reload when inputs can change**: if a value is effectively stable across refresh/reconnect (e.g., app configuration determined by account/environment for the app lifetime), resolve it once at startup and do not refetch it on routine “refresh” actions. Reconnect should retry only when the initial lookup failed.

**Example (generation-based discard)**
```ts
// Per-key generation map
const generationByKey = new Map<string, number>();

function bumpGeneration(key: string) {
  generationByKey.set(key, (generationByKey.get(key) ?? 0) + 1);
}

async function loadAndCache(key: string, fetcher: () => Promise<any>, write: (v: any) => void) {
  const gen = generationByKey.get(key) ?? 0;
  const value = await fetcher();

  // Discard if invalidated since request started
  if ((generationByKey.get(key) ?? 0) !== gen) return;

  write(value);
}

// Example invalidation
function refreshKey(key: string) {
  bumpGeneration(key);
  void loadAndCache(key, () => fetchFromBackend(key), setCacheForKey);
}
```

Adopting this pattern prevents older async reads from overwriting newer cache state, and pairing it with “fetch-once when stable” avoids unnecessary reloads that can otherwise introduce churn or subtle inconsistencies.