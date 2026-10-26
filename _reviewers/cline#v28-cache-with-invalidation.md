---
title: Cache With Invalidation
description: Cache only when you can define (a) the exact dependency key/identity
  for correctness and (b) the precise conditions under which the cached value is invalid.
  Always guard against late async results and cross-scope identity mismatches.
repository: cline/cline#v28
label: Caching
language: TypeScript
comments_count: 4
repository_stars: 70892
---

Cache only when you can define (a) the exact dependency key/identity for correctness and (b) the precise conditions under which the cached value is invalid. Always guard against late async results and cross-scope identity mismatches.

Practical rules:
- Dependency-key correctness: include every input that affects the result (e.g., tool pin definition, tool arguments, plugin registry state/execution mode, account scope/workspace root).
- Version/identity guard: when an async load races with a later change, discard the older result (e.g., per-key “slot” identity or per-scope revision).
- Safe serving window: serve a cached value only while it still matches the current definition (pin still exists and unchanged; lookup key still current; history snapshot TTL only until invalidated).
- Explicit invalidation: when live state changes (or user toggles/refresh happens), invalidate caches before posting UI/state.
- Retry/backoff on failure: if a lookup or load fails, don’t immediately retry forever—wait a bounded backoff/TTL before retrying.

Example pattern (TypeScript):
```ts
type Entry<T> = { value?: T; loadedAt?: number; failedAt?: number; pending?: Promise<void>; slot?: number };

class SafeLookup<T> {
  private entries = new Map<string, Entry<T>>();

  constructor(
    private readonly now: () => number,
    private readonly ttlMs: number,
    private readonly retryBackoffMs: number,
    private readonly load: (key: string) => Promise<T>,
  ) {}

  async get(key: string, refresh = false): Promise<T | undefined> {
    const slot = (this.entries.get(key)?.slot ?? 0) + (refresh ? 1 : 0);
    const e = this.entries.get(key) ?? { slot };

    if (refresh) {
      e.value = undefined;
      e.loadedAt = undefined;
      e.failedAt = undefined;
      e.slot = slot;
      e.pending = undefined;
    }

    const ageOk = e.loadedAt !== undefined && this.now() - e.loadedAt < this.ttlMs;
    if (e.value !== undefined && ageOk) return e.value;

    if (e.pending) return e.value;
    if (e.failedAt !== undefined && this.now() - e.failedAt < this.retryBackoffMs) return e.value;

    const pending = this.load(key).then(
      (value) => {
        const cur = this.entries.get(key);
        if (!cur || cur.slot !== slot) return; // late result; discard
        e.value = value;
        e.loadedAt = this.now();
        e.failedAt = undefined;
        e.pending = undefined;
      },
      () => {
        const cur = this.entries.get(key);
        if (!cur || cur.slot !== slot) return;
        e.failedAt = this.now();
        e.pending = undefined;
      }
    );

    e.pending = pending;
    this.entries.set(key, e);
    await pending;
    return e.value;
  }
}
```
Apply this standard anywhere you cache derived results, inspection results, or remote/live projections: the cache key must encode correctness dependencies, and invalidation/discard rules must prevent stale or late async data from being used.