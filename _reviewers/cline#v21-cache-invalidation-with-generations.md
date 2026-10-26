---
title: Cache invalidation with generations
description: 'When caching async data (file contents, repo snapshots, computed views),
  make cache invalidation explicit and concurrency-safe.


  **Rules**

  1. **Tie invalidation to real inputs**: only drop/reload when the effective cache
  key/input changes (e.g., workspace root, repo snapshot signature). Don’t reload
  stable config during unrelated refreshes.'
repository: cline/cline#v21
label: Caching
language: TSX
comments_count: 3
repository_stars: 70886
---

When caching async data (file contents, repo snapshots, computed views), make cache invalidation explicit and concurrency-safe.

**Rules**
1. **Tie invalidation to real inputs**: only drop/reload when the effective cache key/input changes (e.g., workspace root, repo snapshot signature). Don’t reload stable config during unrelated refreshes.
2. **Guard against late responses**: for each cached entry (or key), maintain a **generation/version token**. Increment the token when you invalidate/drop the cache. When an async response arrives, apply it **only if** its generation still matches.
3. **Handle snapshot polling predictably**: when a new snapshot arrives, mark existing cached entries as **stale**. If a read is already loading, don’t start extra reads immediately—keep the in-flight result (if your policy says so) and schedule **one** follow-up read after completion.
4. **Test the race**: add a test that holds an in-flight read across an invalidation/refresh and asserts the stale response cannot overwrite the fresh contents.

**Sketch**
```ts
const genByKey = new Map<string, number>();

function bump(keys: Iterable<string>) {
  for (const k of keys) genByKey.set(k, (genByKey.get(k) ?? 0) + 1);
}

async function readAndCache(key: string) {
  const gen = genByKey.get(key) ?? 0;
  const result = await fetchSomethingFor(key);
  if ((genByKey.get(key) ?? 0) !== gen) return; // discard superseded response
  cache.set(key, result);
}

// On invalidation:
bump([key]);
void readAndCache(key);
```

Apply this to file/tree content caches and repo-diff caches; and only re-fetch truly variable configuration (otherwise, resolve once and reuse across refresh/reconnect).