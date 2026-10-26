---
title: Versioned cache invalidation
description: When caching async-loaded data, prevent stale responses from overwriting
  fresher state, and avoid unnecessary reloads for values that are stable for the
  app lifetime.
repository: cline/cline#v12
label: Caching
language: TSX
comments_count: 2
repository_stars: 70872
---

When caching async-loaded data, prevent stale responses from overwriting fresher state, and avoid unnecessary reloads for values that are stable for the app lifetime.

**Standard**
1. **Version your cached reads:** attach a monotonically increasing “generation” (or request id) per cache entry key (e.g., file path).
2. **Invalidate by bumping generation:** when dropping/refreshing cache for a key (refresh, tab close, external edit), increment the generation for that key.
3. **Discard superseded results:** when an async call resolves, update state only if the generation/request id still matches the latest for that key.
4. **Test the race:** add a test that keeps a read in-flight across an invalidation/refresh and asserts the stale response can’t replace the new contents.
5. **Don’t reload stable configuration on refresh:** for data effectively immutable within the process lifetime (e.g., app base URL tied to the backend/environment), resolve it once during startup/initialization; reconnect should only retry the initial lookup if it previously failed.

**Example (generation-based async cache)**
```ts
// Map: key -> { generation, value }
const cache = new Map<string, { generation: number; value?: string }>();

async function load(key: string) {
  const current = cache.get(key) ?? { generation: 0 };
  const myGen = current.generation;

  const value = await fetchForKey(key);

  // Only apply if nothing invalidated since we started
  const latest = cache.get(key);
  if (!latest || latest.generation !== myGen) return;

  cache.set(key, { ...latest, value });
}

function invalidate(key: string) {
  const current = cache.get(key) ?? { generation: 0 };
  cache.set(key, { ...current, generation: current.generation + 1, value: undefined });
}
```

Apply this pattern to prevent stale async overwrites (correctness/performance) and limit cache churn by resolving truly stable dependencies once per lifecycle (rather than on every refresh/reconnect).