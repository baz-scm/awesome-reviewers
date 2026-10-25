---
title: Dependency-Aware Caching
description: Caching is safe only when you (1) key by the full dependency set, (2)
  gate reads by a revision/stale check, (3) invalidate only the correct scope, and
  (4) handle async failures with rollback + bounded retries.
repository: ClInE/cLiNe
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70838
---

Caching is safe only when you (1) key by the full dependency set, (2) gate reads by a revision/stale check, (3) invalidate only the correct scope, and (4) handle async failures with rollback + bounded retries.

**Standards**
1. **Include all dependencies in the cache key**
   - If the cached value depends on inputs (tool id, arguments, account scope, workspace root, repo+branch, execution mode), those must be part of the key.
   - For unordered structures (e.g., argument objects), use an order-insensitive representation.
2. **Add a revision/stale gate for correctness**
   - If the underlying definition can change (pin edited/removed, UI set refreshed, plugin registry state updated), store a revision and only serve cached results while the revision still matches.
3. **Scope your invalidation**
   - Invalidate/recompute only for the affected workspace/account/session/query. Do not let a single lookup failure poison shared availability caches.
4. **Protect caches with explicit budgets and eviction**
   - Use explicit TTL or idle eviction, and/or max-bytes (LRU or “refresh on read”).
   - Keep caches session-scoped when the URI or data should not cross boundaries.
5. **Retry boundedly after failures—especially when detection is imperfect**
   - If a failure recovery cannot be detected by fingerprinting/key changes, retry on a bounded backoff (e.g., “every 30s max”), and don’t let repeated attempts stack.
6. **When updating stale state asynchronously, use rollback**
   - If you clear a “stale”/“needs rebuild” flag before kicking an async operation, restore it if the operation throws so retries behave correctly.

**Practical pattern (keyed async lookup with TTL + backoff)**
```ts
class KeyedLookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;
  constructor(
    private readonly now: () => number,
    private readonly onLoaded: () => void,
    private readonly retryMs: number,
  ) {}

  async get(key: string, load: () => Promise<T>, refresh = false): Promise<T | undefined> {
    this.start(key, load, refresh);
    await this.pending;
    return this.value;
  }

  private start(key: string, load: () => Promise<T>, refresh: boolean) {
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }
    if (this.value !== undefined) return;
    if (this.pending) return;
    if (this.failedAt !== undefined && this.now() - this.failedAt < this.retryMs) return;

    const pending = load().then(
      (v) => {
        if (this.pending !== pending) return;
        this.pending = undefined;
        this.value = v;
        this.onLoaded();
      },
      () => {
        if (this.pending !== pending) return;
        this.pending = undefined;
        this.failedAt = this.now();
      }
    );
    this.pending = pending;
  }
}
```

**Checklist before landing a cache change**
- What exact inputs determine the value? Are they in the cache key?
- Can those inputs change while an async operation is in-flight? Do you need a revision gate?
- What should happen if loading fails: invalidate, rollback a stale flag, or schedule bounded retry?
- What scope must stay isolated (account/workspace/session)?
- What eviction strategy/budget prevents unbounded memory growth?