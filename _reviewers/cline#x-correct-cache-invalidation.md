---
title: Correct Cache Invalidation
description: Cache only when the entry matches the full identity of what produced
  it, and invalidate/expire aggressively when identity or scope can change—while deduplicating
  in-flight refreshes and backing off on failures.
repository: cline/cline#x
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70861
---

Cache only when the entry matches the full identity of what produced it, and invalidate/expire aggressively when identity or scope can change—while deduplicating in-flight refreshes and backing off on failures.

Apply this checklist:
- **Key the cache by all invalidation-relevant inputs** (not just “what you asked for”): include arguments normalized for order when needed, session identity (e.g., sessionId in URIs), plugin registry state, and current scope/account generation.
- **Gate serving by identity match**: if the underlying definition changes (pin revision edited/removed, account scope switched), never serve old results—return nothing or a “miss” until recomputed.
- **Use scope/generation guards** around async work so late completions can’t overwrite newer state.
- **Deduplicate concurrent loads** with a single in-flight promise per cache key.
- **Expire with bounded TTLs** to avoid long-lived stale snapshots.
- **On failure, don’t permanently poison**: release/clear the “warm-up” handle and retry later with backoff (and ensure failures don’t invalidate unrelated caches).

Example pattern (identity + in-flight dedupe + TTL + generation):
```ts
class KeyedCache<T> {
  private value = new Map<string, {v: T; at: number}>();
  private inFlight = new Map<string, Promise<T>>();
  private generation = 0;
  constructor(private readonly ttlMs: number) {}

  setGeneration() { this.generation++; }

  async get(key: string, load: (gen: number) => Promise<T>): Promise<T> {
    const now = Date.now();
    const cached = this.value.get(key);
    if (cached && now - cached.at < this.ttlMs) return cached.v;

    const existing = this.inFlight.get(key);
    if (existing) return existing;

    const gen = this.generation;
    const p = load(gen)
      .then((v) => {
        // Drop late results from older generations.
        if (gen !== this.generation) return Promise.reject(new Error('stale'));
        this.value.set(key, { v, at: Date.now() });
        return v;
      })
      .catch((e) => {
        // Clear failure so the next caller can retry (possibly with backoff elsewhere).
        throw e;
      })
      .finally(() => {
        if (this.inFlight.get(key) === p) this.inFlight.delete(key);
      });

    this.inFlight.set(key, p);
    return p;
  }
}
```

Teams should treat “cache correctness” as first-class: every cache entry must be traceable to the exact inputs that would make it invalid, and every async refresh must be protected against late/stale completion.