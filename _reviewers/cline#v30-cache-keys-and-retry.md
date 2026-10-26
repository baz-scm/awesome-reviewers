---
title: Cache Keys And Retry
description: 'Make caching correctness-driven: every cached result must be uniquely
  identified by the full set of inputs that can change it, and caches must have explicit
  invalidation and bounded retry behavior for failures.'
repository: cline/cline#v30
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70894
---

Make caching correctness-driven: every cached result must be uniquely identified by the full set of inputs that can change it, and caches must have explicit invalidation and bounded retry behavior for failures.

Apply these rules:
1) **Use complete cache keys**
   - Include *scope* (account/workspace), *mode/execution mode*, and any *upstream registry state* that affects the computed output.
   - If a toggle/enable/disable changes what would be discovered, ensure the cache key changes too.
2) **Invalidate when live data changes**
   - When a background status/record changes, call the corresponding cache invalidation before/when projecting new state.
3) **TTL/age-out with non-flicker reloads**
   - In distributed systems, keep serving the last cached value until the age-out window ends, then reload behind it.
4) **Negative caching with backoff + escape hatch**
   - For failed reads/imports, cache the failure for a fixed window (e.g., 30s), retry after the window, and allow an explicit refresh to bypass the backoff.
   - Bound retries so you don’t loop forever after an “invisible” fix.
5) **Prevent cache breakage from serialization/parsing mismatches and identity aliasing**
   - Ensure your cache serialization/parsing matches the real schema (e.g., `mimeType` vs `mediaType`).
   - If identifiers can alias/rebind (e.g., thread vs runtime session IDs), ensure the cache key reflects the identity actually used by the reader.

Example pattern (complete key + TTL + negative backoff):
```ts
class TimedCache<T> {
  private value?: T;
  private key?: string;
  private pending?: Promise<void>;
  private failedAt?: number;
  private lastFetchedAt = 0;

  constructor(
    private readonly now: () => number,
    private readonly ttlMs: number,
    private readonly retryMs: number,
  ) {}

  async get(key: string, load: () => Promise<T>, refresh = false): Promise<T | undefined> {
    // key changes always discard
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
      this.lastFetchedAt = 0;
    }

    if (this.value !== undefined && !refresh && this.now() - this.lastFetchedAt < this.ttlMs) {
      return this.value;
    }

    if (this.pending) return this.value;
    if (this.failedAt !== undefined && this.now() - this.failedAt < this.retryMs) return this.value;

    this.pending = load()
      .then(v => {
        this.value = v;
        this.lastFetchedAt = this.now();
        this.failedAt = undefined;
      })
      .catch(() => {
        this.failedAt = this.now();
      })
      .finally(() => {
        this.pending = undefined;
      });

    await this.pending;
    return this.value;
  }
}
```