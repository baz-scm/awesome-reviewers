---
title: Versioned Cache Keys
description: 'When caching, make correctness the first goal: cache entries must be
  keyed by the exact dependencies that affect the value, and async writes must be
  rejected if the dependencies changed while the request was in flight.'
repository: cline/cline#v7
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70865
---

When caching, make correctness the first goal: cache entries must be keyed by the exact dependencies that affect the value, and async writes must be rejected if the dependencies changed while the request was in flight.

Practical rules:
1) Key by inputs + revision/state
- If the cached value depends on tool name *and arguments*, the key must include both (and be robust to argument order when appropriate).
- If the cached value depends on configuration/plugin registry status, include that status in the cache key.

2) Guard against stale async completion
- Before committing a computed result into the cache, verify the current revision/generation still matches the revision/generation used to start the computation.
- If it no longer matches, drop the result.

3) Invalidate or “serve nothing” on dependency mismatch
- Don’t serve cached results after a pin/filter/selection changes unless you can prove they still apply (e.g., label-only edits may be allowed).

4) Use TTL and backoff for eventual consistency/failures
- For list-like caches, use TTL to reduce load.
- For failed loads/imports, remember the failure briefly and retry on a backoff even if the fingerprint/key is unchanged (to recover from “invisible” fixes).

5) Don’t rewrite stabilized artifacts unnecessarily
- If you already stored a shortened/persisted representation, later retries/resumes should reuse it rather than re-truncate or re-rewrite.

Pattern (stale-async guard):
```ts
class Cache<T> {
  private map = new Map<string, { revision: number; value: T }>();
  private revision = 0;

  updateRevision() { this.revision += 1; }

  async refresh(key: string, compute: (revision: number) => Promise<T>) {
    const revAtStart = this.revision;
    const value = await compute(revAtStart);
    if (this.revision !== revAtStart) return; // stale in-flight result
    this.map.set(key, { revision: revAtStart, value });
  }
}
```
Adopt this standard for caches that combine stateful UI selections, distributed/session data, plugin inspection/loading, and persisted tool-output recovery.