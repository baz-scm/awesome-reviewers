---
title: Correct Cache Keys
description: 'When caching derived results, ensure the cache is *provably correct
  for the inputs that produced it* and *bounded when correctness is uncertain*.


  **Standards**'
repository: cline/cline#v16
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70882
---

When caching derived results, ensure the cache is *provably correct for the inputs that produced it* and *bounded when correctness is uncertain*.

**Standards**
1. **Key by the full dependency set**
   - Include every input that can change the output (e.g., pin tool + arguments; lookup key = account scope + workspace root + repo+branch; plugin inspection key includes registry state and execution mode).
2. **Add a revision/generation guard for definition/scope drift**
   - If the upstream definition can change while the async work is in flight, attach a monotonic revision/generation and only serve results when it still matches.
3. **Use TTL / bounded staleness for list/history caches**
   - Cache snapshots briefly; refresh after TTL or scope transition. Prefer “generation” checks to prevent cross-scope attribution.
4. **Handle failure caches with backoff (negative caching)**
   - Cache “failed to load” outcomes only for a bounded retry window; retry even when the invalidation signal is invisible (e.g., fingerprint unchanged).
5. **Invalidate before publishing state**
   - When toggles affect what downstream caches will show, invalidate caches first, then post state/UI updates.

**Pattern (TypeScript)**
```ts
type CacheEntry<T> = {
  value?: T;
  updatedAt: number;
  revision: number;      // or generation
  failedAt?: number;    // for negative cache
};

const TTL_MS = 10_000;
const RETRY_MS = 30_000;

class CachedResolver<T> {
  private entry?: CacheEntry<T>;
  private revision = 0;

  // call when upstream definition/scope changes
  bumpRevision() { this.revision++; }

  async get(currentKey: string, load: () => Promise<T>): Promise<T | undefined> {
    const now = Date.now();
    const e = this.entry;

    // Serve only if key matches and TTL not expired and revision still current.
    if (e && e.revision === this.revision && e.value !== undefined && now - e.updatedAt < TTL_MS) {
      return e.value;
    }

    // Negative cache backoff.
    if (e && e.revision === this.revision && e.failedAt !== undefined && now - e.failedAt < RETRY_MS) {
      return undefined;
    }

    try {
      const value = await load();
      this.entry = { value, updatedAt: now, revision: this.revision };
      return value;
    } catch {
      // keep the failure bounded so we don’t permanently poison the cache
      this.entry = { value: e?.value, updatedAt: e?.updatedAt ?? 0, revision: this.revision, failedAt: now };
      return undefined;
    }
  }
}
```

Adopting this standard prevents the common failure modes seen across the discussed code: stale results after pin/definition drift, cross-scope cache attribution, UI mismatches due to missing invalidation, and permanent “stuck” failures without bounded retry.