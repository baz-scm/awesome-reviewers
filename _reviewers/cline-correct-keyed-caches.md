---
title: Correct Keyed Caches
description: Cache only when you can prove the cached value still matches the current
  “identity” of the request/state, and always have a bounded strategy for refresh/retry.
repository: cline/CLINE
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70839
---

Cache only when you can prove the cached value still matches the current “identity” of the request/state, and always have a bounded strategy for refresh/retry.

**Standards**
1. **Key by full identity, not just “what you wanted”.** Include all inputs and any revision/version that affects meaning (e.g., pin tool+arguments, execution mode, plugin registry state, account/workspace scope, repository+branch).
2. **Guard against late async responses.** Don’t overwrite/serve when the request identity has changed since the request started. Use revision counters or identity equality checks.
3. **Invalidate on explicit state transitions.** When toggles/permissions/scope change, invalidate dependent caches *before* publishing new state.
4. **Use TTL for “staleness tolerances”, but refresh in the background.** Past-ttl reads may be served briefly to avoid UI flicker, while a reload runs behind it.
5. **Failures need their own bounded retry policy.** Remember failure and retry after a delay; if the change might be “invisible to fingerprints”, still retry periodically (with backoff) until the system can observe recovery.
6. **Change detection via fingerprints when relevant.** For plugin/source caches, compute fingerprints over the actually-reachable static graph (including side-effect imports) and include execution context in the cache key.

**Example pattern (key + late-response guard + backoff retry)**
```ts
type CacheEntry<T> = { key: string; value?: T; pending?: Promise<T>; failedAt?: number };

const FAILURE_RETRY_MS = 30_000;

class KeyedCache<T> {
  private entry: CacheEntry<T> = { key: "" };

  async get(key: string, load: () => Promise<T>): Promise<T | undefined> {
    // Cache identity changed => reset.
    if (this.entry.key !== key) {
      this.entry = { key };
    }

    // Success already known.
    if (this.entry.value !== undefined) return this.entry.value;

    // Backoff after failure.
    if (this.entry.failedAt !== undefined && Date.now() - this.entry.failedAt < FAILURE_RETRY_MS) {
      return undefined;
    }

    // De-dupe concurrent loads.
    if (this.entry.pending) return this.entry.value;

    const pending = load().then(
      (value) => {
        // Late-response guard: only commit if identity still matches.
        if (this.entry.key === key) this.entry = { key, value };
        return value;
      },
      () => {
        if (this.entry.key === key) this.entry.failedAt = Date.now();
        return undefined;
      }
    );

    this.entry.pending = pending;
    return undefined;
  }
}
```
Apply these rules consistently across memory caches, persisted caches, and distributed caches to prevent stale data, unblock recovery from transient/opaque failures, and keep UI/state projections coherent.