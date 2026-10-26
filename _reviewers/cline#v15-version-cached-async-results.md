---
title: Version Cached Async Results
description: When you cache data that is loaded asynchronously (e.g., directory/file
  contents, lookups), prevent in-flight/stale responses from overwriting newer state.
repository: cline/cline#v15
label: Caching
language: TSX
comments_count: 2
repository_stars: 70877
---

When you cache data that is loaded asynchronously (e.g., directory/file contents, lookups), prevent in-flight/stale responses from overwriting newer state.

**Rule of thumb**
1. **Tag cached reads with a version/generation.** Increment/bump the generation whenever you invalidate/drop the cache entry (refresh, close tab, external edit, etc.).
2. **Discard superseded responses.** When an async call resolves, apply it only if its generation still matches the latest generation for that cache key/path.
3. **Only reload when invalidation is real.** If the underlying value is invariant for the app lifetime (e.g., derived config that won’t change after a successful startup lookup), compute once and keep it across account refreshes/reconnects.
4. **Test the race.** Add a test that keeps a read “in flight” across an invalidation and asserts the stale response cannot replace fresh contents.

**Example pattern (generation token)**
```ts
const generations = new Map<string, number>();
const [cache, setCache] = useState(new Map<string, { value: unknown }>());

function bumpGeneration(key: string) {
  const next = (generations.get(key) ?? 0) + 1;
  generations.set(key, next);
  return next;
}

async function readWithCache(key: string) {
  const gen = generations.get(key) ?? 0;

  // Drop/refresh elsewhere should bump generation.
  const result = await fetchSomeAsyncData(key);

  // Apply only if not superseded.
  if ((generations.get(key) ?? 0) !== gen) return;

  setCache((current) => {
    const next = new Map(current);
    next.set(key, { value: result });
    return next;
  });
}

function invalidate(key: string) {
  bumpGeneration(key);
  // Optionally clear cache entry here.
  setCache((current) => {
    const next = new Map(current);
    next.delete(key);
    return next;
  });
}
```

Adopting this ensures your caching layer is correct under concurrency, and it avoids unnecessary reloads when values are effectively static.