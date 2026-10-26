---
title: Cache Invalidation Rules
description: 'When adding or changing caching, require these properties:


  1) Key correctness (invalidate what matters)

  - Include every dimension that can change results: scope/account/workspace identifiers,
  execution mode, and any cache-relevant plugin/session state.'
repository: cline/cline#v14
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70876
---

When adding or changing caching, require these properties:

1) Key correctness (invalidate what matters)
- Include every dimension that can change results: scope/account/workspace identifiers, execution mode, and any cache-relevant plugin/session state.
- If content can change without obvious timestamps, use a deterministic fingerprint derived from the inputs you actually rely on (e.g., reachable static import sources), and put that fingerprint (or the derived “state”) into the cache key.

2) Bounded staleness (TTL/age-out)
- Never cache indefinitely. Use TTL/age-out so permissions/config changes eventually appear.
- Prefer “background refresh behind the scenes” to avoid UI flicker: keep serving cached values until the new load completes, then publish.

3) Failure retry/backoff (when invalidation can’t detect fixes)
- If a cached failure can become resolvable without changing the detectable inputs (e.g., the fix is “invisible” to your fingerprint), remember the failure timestamp and retry after a fixed backoff.
- Bound retries (rate limit) so the system doesn’t thrash.

4) Distributed/multi-window authority (merge/prune)
- For shared state across processes/windows, define an authority model (source-of-truth) and implement merge rules that only allow monotonic growth or explicit pruning for deleted entities.
- Drop stale/deleted entries on write so old snapshots don’t permanently resurrect removed data.

5) Safe reads + bounded eviction
- Enforce ownership/scope on reads (e.g., validate URI/sessionId matches the current runtime).
- Apply explicit bounds (max bytes/size, idle eviction, or LRU behavior) to prevent memory/disk runaway.

Example pattern (keyed cache with TTL and failure backoff)
```ts
const LOOKUP_RETRY_MS = 30_000;
const CACHE_TTL_MS = 60_000;

class Lookup<T> {
  private key?: string;
  private value?: T;
  private loadedAt?: number;
  private pending?: Promise<void>;
  private failedAt?: number;

  constructor(private now: () => number, private onLoaded: () => void) {}

  async get(key: string, load: () => Promise<T>, refresh: boolean): Promise<T | undefined> {
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.loadedAt = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }

    if (this.value !== undefined && this.loadedAt !== undefined && (this.now() - this.loadedAt) < CACHE_TTL_MS) {
      return this.value;
    }
    if (this.pending) return (this.pending as Promise<void>).then(() => this.value);
    if (this.failedAt !== undefined && this.now() - this.failedAt < LOOKUP_RETRY_MS) return this.value;

    this.pending = load().then(
      (v) => {
        if (this.pending == null) return;
        this.value = v;
        this.loadedAt = this.now();
        this.failedAt = undefined;
        this.pending = undefined;
        this.onLoaded();
      },
      () => {
        if (this.pending == null) return;
        this.failedAt = this.now();
        this.pending = undefined;
      }
    );

    await this.pending;
    return this.value;
  }
}
```
Apply this checklist to any cache used for plugins, cloud/session history, tool outputs, or distributed UI state so correctness, freshness, and recovery behavior are explicit rather than accidental.