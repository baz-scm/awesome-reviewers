---
title: Cache with Versioning
description: 'Cache only when you can prove the cached value still matches the current
  inputs/definition, and make invalidation explicit.


  Apply these rules:

  1) Key caches by the true dependency tuple'
repository: cline/cline#v26
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70893
---

Cache only when you can prove the cached value still matches the current inputs/definition, and make invalidation explicit.

Apply these rules:
1) Key caches by the true dependency tuple
- Include identifiers and parameters that change the result (e.g., tool id + normalized arguments; account/workspace/repo+branch).
- Normalize key order/shape so semantically identical inputs map to the same key.

2) Prefer revision/generation invalidation over “eventual refresh”
- If you can track a revision/version (pin revision, UI set revision, scope generation), gate serving and drop/withhold stale entries when the revision no longer matches.

3) Never serve stale data to stateful actions
- For any “use/send/execute” tied to a cached set, refuse the action unless the current revision and the item id still match.

4) Treat failures as first-class cache states
- Cache failure results (so repeated calls don’t thrash), but attach a timestamp and retry after a bounded backoff.
- If your cache invalidation can miss fixes (fingerprint unchanged, dynamic/import edge cases), use a time-based retry even when the key didn’t change.

5) TTL is for rate-limiting, not correctness
- Use TTL to cap refresh frequency; don’t rely on TTL alone when correctness depends on explicit versioning.

Example pattern (pin/tool-result style):
```ts
type CacheEntry = { fetchedAt: number; value: string; version: string };
const cache = new Map<string, CacheEntry>();

function normalizeArgs(args: Record<string, unknown>): string {
  // stable serialization so key order does not change the cache key
  return JSON.stringify(Object.entries(args).sort(([a],[b]) => a.localeCompare(b)));
}

function cacheKey(tool: string, args: Record<string, unknown>, pinVersion: string): string {
  return `${tool}:${normalizeArgs(args)}:${pinVersion}`;
}

function getIfStillValid(key: string, currentVersion: string): string | undefined {
  const entry = cache.get(key);
  return entry && entry.version === currentVersion ? entry.value : undefined; // drop stale
}
```

Use the same structure everywhere you have caching: inputs → stable key → explicit version gate → failure/backoff retry when correctness can’t be inferred from the key alone.