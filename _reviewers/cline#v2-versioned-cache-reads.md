---
title: Versioned Cache Reads
description: 'When caching async data, treat cache invalidation and reload boundaries
  as first-class:


  1) Prevent stale async overwrites: associate each cached key with a monotonically
  increasing “generation” (version) and discard any in-flight response whose generation
  no longer matches the latest value.'
repository: cline/cline#v2
label: Caching
language: TSX
comments_count: 2
repository_stars: 70861
---

When caching async data, treat cache invalidation and reload boundaries as first-class:

1) Prevent stale async overwrites: associate each cached key with a monotonically increasing “generation” (version) and discard any in-flight response whose generation no longer matches the latest value.
2) Avoid unnecessary reloads: only refetch cached/config values when the underlying inputs can change. If a value is fixed for the app’s lifetime (e.g., resolved backend/app base URL), resolve it once at startup/reconnect bootstrap and reuse it across account refreshes.

Example pattern (generation token):

```ts
// Per-key generation map
const genByKey = new Map<string, number>();

function bumpGeneration(key: string) {
  genByKey.set(key, (genByKey.get(key) ?? 0) + 1);
  return genByKey.get(key)!;
}

async function readWithStaleDiscard<T>(key: string, fetcher: () => Promise<T>) {
  const myGen = bumpGeneration(key);
  const result = await fetcher();

  // Only commit if still the latest generation for this key
  if (genByKey.get(key) !== myGen) return;
  return result; // safe to write into cache/state
}
```

Example reload boundary rule:
- If an account refresh is triggered frequently but the backend/app mapping is fixed for the app lifetime, do not re-request it inside `refreshAccount`; perform the lookup once during initial bootstrap (with reconnect logic only to retry a failed initial lookup).