---
title: Generation-based cache coherency
description: 'When caching data that can be reloaded asynchronously (especially under
  polling/refresh), ensure cache invalidation is concurrency-safe.


  Apply these rules:'
repository: cline/cline#v28
label: Caching
language: TSX
comments_count: 3
repository_stars: 70893
---

When caching data that can be reloaded asynchronously (especially under polling/refresh), ensure cache invalidation is concurrency-safe.

Apply these rules:
1) Cache long-lived configuration once: if environment/backend inputs are stable for the app (or feature) lifetime, resolve them at startup and avoid reloading on unrelated refresh/reconnect events.
2) Invalidate by epoch/version: when you “drop” or refresh a cached entry (or snapshot arrives), increment a per-key (or per-path) generation/epoch.
3) Guard async responses: capture the generation at the time a read is initiated; when the response arrives, discard it if the generation no longer matches the current one.
4) Use stale-while-revalidate for UX: on snapshot/refresh, mark cached items as stale and keep rendering, but trigger a follow-up read using the same generation/invalidations so late responses can’t overwrite fresh ones.
5) Test the race: add tests that keep an in-flight read open across refresh/polling and assert that only the expected follow-up read updates the cache.

Example pattern (per-key generation):
```ts
const generationByKey = new Map<string, number>();
const invalidate = (keys: Iterable<string>) => {
  for (const k of keys) {
    generationByKey.set(k, (generationByKey.get(k) ?? 0) + 1);
  }
};

async function readWithGuard<T>(key: string, fetcher: () => Promise<T>): Promise<T | null> {
  const gen = generationByKey.get(key) ?? 0;
  const result = await fetcher();
  const currentGen = generationByKey.get(key) ?? 0;
  if (currentGen !== gen) return null; // discard stale/out-of-order response
  return result;
}
```