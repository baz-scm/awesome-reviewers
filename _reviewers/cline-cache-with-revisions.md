---
title: Cache with Revisions
description: 'Cache only what you can prove is still valid.


  **Standards**

  1. **Key by semantic inputs, not just “request type”**: include all parameters that
  affect the result (e.g., pinned read key must include tool + arguments; cache lookup
  key must include account scope + workspace root + repo+branch).'
repository: CLINE/cline
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70839
---

Cache only what you can prove is still valid.

**Standards**
1. **Key by semantic inputs, not just “request type”**: include all parameters that affect the result (e.g., pinned read key must include tool + arguments; cache lookup key must include account scope + workspace root + repo+branch).
2. **Use authoritative versioning for invalidation**: when the underlying definition can change, tie cache serving to a **revision/generation** (pin revision, scope/account generation). TTL alone is not enough.
3. **Prevent cross-scope leakage**: guard cached entries and async updates with a generation/scope token; discard results if the context changed while promises were in flight.
4. **Invalidate dependent caches before posting state**: if a setting/feature toggle changes what history/loaders should include, invalidate the affected cache first, then publish state.
5. **Apply negative caching with backoff for failures**: remember failed loads and retry after a bounded delay. Also retry when failures might become resolvable without changing the detected fingerprint (use backoff even if key/fingerprint is unchanged).

**Pattern (TypeScript-style)**
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
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }
    if (this.value !== undefined) return this.value;
    if (this.pending) return undefined;
    if (this.failedAt !== undefined && this.now() - this.failedAt < this.retryMs) return undefined;

    const pending = load().then(v => {
      if (this.pending !== pending) return;
      this.pending = undefined;
      this.value = v;
      this.onLoaded();
    }).catch(() => {
      if (this.pending !== pending) return;
      this.pending = undefined;
      this.failedAt = this.now(); // negative cache + backoff
    });

    this.pending = pending;
    return undefined;
  }
}
```

**Application tips**
- For caches keyed by objects/args, normalize the key (e.g., ignore argument key order).
- When serving cached values during async refresh, ensure the refresh result is only applied if the **revision/generation still matches**.
- Cache entries representing “loaded plugin state / discovery results” should include the **plugin execution mode and registry state** in the cache fingerprint so turning plugins on/off invalidates correctly.