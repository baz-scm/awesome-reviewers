---
title: Cache Key, TTL, Retry
description: 'Caching should be safe by construction: choose a key that fully captures
  observable inputs, refresh with TTL in a non-flickering way, and add bounded retry
  when failures can be “invisible” to your invalidation signal.'
repository: cline/cline#v11
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70871
---

Caching should be safe by construction: choose a key that fully captures observable inputs, refresh with TTL in a non-flickering way, and add bounded retry when failures can be “invisible” to your invalidation signal.

Rules of thumb:
- **Key correctness:** Include all dimensions that affect outputs (e.g., plugin set/state, execution mode, session/account scope, model selection source). If a change can alter behavior but doesn’t change your key, you’ll ship stale behavior.
- **TTL + background refresh:** When data is expensive to compute/load, serve the cached value until TTL expires, then reload **behind the scenes** and update observers/state once the reload succeeds. Avoid clearing the cache eagerly (prevents UI flicker).
- **Failure recovery with backoff:** If cache invalidation relies on best-effort detection (fingerprints, directory scans, etc.), assume there are cases you can’t detect. When a load fails, **remember the failure** and **retry after a fixed/backoff interval**, but cap frequency.
- **Distributed/stale state:** If “authority” is persisted/merged across windows/processes, implement merge+prune so deleted entities don’t keep stale authority. Prefer re-reading from disk on refresh rather than relying on in-memory snapshots.
- **Cache identity matches runtime binding:** Ensure cache keys represent the runtime identity you actually re-open later (e.g., session/thread IDs can diverge; mismatched identity strands cached drafts).

Example pattern (TTL + background refresh + key-based slotting):
```ts
const TTL_MS = 60_000;

class Lookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;

  constructor(private readonly now: () => number,
              private readonly onLoaded: () => void) {}

  async get(key: string, load: () => Promise<T>): Promise<T | undefined> {
    // Slot by key
    if (this.key !== key) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }
    // Retry backoff on failures
    if (this.value !== undefined) {
      return this.value;
    }
    if (this.pending) return undefined;
    if (this.failedAt !== undefined && this.now() - this.failedAt < TTL_MS) return undefined;

    this.pending = load().then(v => {
      if (this.key !== key) return; // dropped by a newer key
      this.value = v;
      this.failedAt = undefined;
      this.pending = undefined;
      this.onLoaded();
    }).catch(() => {
      if (this.key !== key) return;
      this.failedAt = this.now();
      this.pending = undefined;
    });

    await this.pending;
    return this.value;
  }
}
```
Apply this approach to your caches: (1) compute a correct key, (2) TTL-age and refresh behind the scenes, (3) retry failures with backoff when invalidation signals may be insufficient.