---
title: Cache Correctness Rules
description: 'When caching async or state-derived results, treat the cache as a correctness
  mechanism, not a performance hack:


  - Define a semantic cache key: include all inputs that affect the cached meaning
  (e.g., account scope + workspace + repo+branch; pin tool+args; plugin path + execution
  mode + plugin registry state).'
repository: cline/cline#v13
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70874
---

When caching async or state-derived results, treat the cache as a correctness mechanism, not a performance hack:

- Define a semantic cache key: include all inputs that affect the cached meaning (e.g., account scope + workspace + repo+branch; pin tool+args; plugin path + execution mode + plugin registry state).
- Invalidate by meaning boundaries, not by time alone: clear/replace cached entries when the semantic key changes; ensure late/obsolete async responses don’t overwrite newer state.
- Make “stale”/sentinel flags rollback-safe: if a refresh/rebuild fails, restore the previous sentinel so subsequent reads retry (avoid permanent “stale cleared” or “ready when not ready” states).
- Add explicit failure and retry policy: 
  - remember failures with a timestamp,
  - retry after a bounded backoff,
  - avoid infinite retry loops,
  - cap retries to what’s user-visible.
- Publish state only when the underlying cache is actually populated: warmups should not “lock in” fallbacks if the cache isn’t filled.

Code sketch (lookup cache with meaning-key + rollback-safe refresh/backoff):

```ts
const LOOKUP_RETRY_MS = 30_000;

class Lookup<T> {
  private key?: string;
  private value?: T;
  private failedAt?: number;
  private pending?: Promise<void>;

  constructor(private readonly now: () => number,
              private readonly load: (key: string) => Promise<T>,
              private readonly onLoaded: () => void) {}

  async get(key: string, refresh: boolean): Promise<T | undefined> {
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.failedAt = undefined;
      this.pending = undefined;
    }

    if (this.value !== undefined) return this.value;
    if (this.pending) return undefined;
    if (this.failedAt !== undefined && this.now() - this.failedAt < LOOKUP_RETRY_MS) return undefined;

    const slot = this.pending = this.load(key)
      .then(v => {
        if (this.pending !== slot) return;
        this.pending = undefined;
        this.value = v;
        this.onLoaded();
      })
      .catch(() => {
        if (this.pending !== slot) return;
        this.pending = undefined;
        this.failedAt = this.now();
      });

    return undefined;
  }
}

// Rollback-safe sentinel example:
async function refreshWithRollback(setStale: () => void, clearStale: () => void, rebuild: () => Promise<void>) {
  clearStale();
  try {
    await rebuild();
  } catch (e) {
    setStale(); // restore so next request retries
    throw e;
  }
}
```

Practical checklist for PRs in this area:
- What is the semantic key? Does it include revisions/state, and is it stable (e.g., ignore argument order)?
- What prevents late async results from overwriting newer state?
- What happens on refresh/rebuild failure—do sentinels rollback?
- How are failures retried (backoff + upper bound)?
- Are warmups allowed to publish only when the cache is truly populated?
- Are there tests covering: failure rollback, late-response suppression, and retry-after-backoff behavior?