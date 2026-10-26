---
title: Identity-Bound Cache Invalidation
description: 'When caching, bind every cached value to the *identity/version* of the
  inputs it depends on, and ensure async completions can’t write stale results.


  Practical rules:'
repository: cline/cline#v29
label: Caching
language: TypeScript
comments_count: 5
repository_stars: 70893
---

When caching, bind every cached value to the *identity/version* of the inputs it depends on, and ensure async completions can’t write stale results.

Practical rules:
1) **Key by full input identity**: include all fields that affect the result (e.g., tool name + normalized arguments; include plugin registry/updatedAt/state; include account scope + workspace/repo/branch).
2) **Use revision/generation guards for async**: store a `revision/generation/key` when you start a load; when the promise resolves, write to cache only if the current revision/key still matches.
3) **Invalidate on relevant changes**: on pin edits/removals, scope transitions, plugin enable/disable, or UI refresh/revision, discard or refuse to use cached data tied to the old identity.
4) **Refuse stale actions**: if a UI action targets an item from an older cached set, respond “stale”/refuse rather than acting.
5) **Add TTL/negative caching only after correctness**: rate-limit retries and cache negative outcomes (with timestamps) to avoid thundering herds, but never let TTL paper over identity mismatches.

Example pattern (async cache with identity guard):
```ts
class KeyedCache<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;
  constructor(private readonly now: () => number,
              private readonly write: (v: T) => void) {}

  async load(key: string, fetch: () => Promise<T>, refresh = false) {
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }
    if (this.value !== undefined) return this.value;

    const startKey = this.key; // identity snapshot
    this.pending ??= (async () => {
      try {
        const v = await fetch();
        if (this.key !== startKey) return; // late completion guard
        this.value = v;
        this.write(v);
      } catch {
        if (this.key !== startKey) return; // late completion guard
        this.failedAt = this.now();
      } finally {
        this.pending = undefined;
      }
    })();

    await this.pending;
    return this.value;
  }
}
```
Apply this pattern to caches/projections/lookup loaders and to UI “cached set” lifecycles (refuse stale actions unless the revision+item id still match).