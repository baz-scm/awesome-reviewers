---
title: Cache With Validity Windows
description: When caching computed data, ensure each cache entry has (a) a semantic
  key/version so results can be served only while inputs still match, (b) an explicit
  invalidation/refresh policy (TTL + background reload), and (c) explicit handling
  for refresh/load failures (rollback/restore and bounded retry), rather than letting
  “stale” or “failed” states persist...
repository: cline/cline#v8
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70867
---

When caching computed data, ensure each cache entry has (a) a semantic key/version so results can be served only while inputs still match, (b) an explicit invalidation/refresh policy (TTL + background reload), and (c) explicit handling for refresh/load failures (rollback/restore and bounded retry), rather than letting “stale” or “failed” states persist forever.

**Do**
- **Key by all semantics-affecting inputs**: include arguments (not just IDs), account/workspace scope, and execution mode.
- **Use validity windows**: either a TTL or an external revision (e.g., pin revision) so “serve cached” is justified.
- **Background refresh without flicker**: return the last cached value immediately, but reload behind the scenes once expired.
- **Failure rollback/restore**: if you must clear a staleness marker before a rebuild, restore it if rebuild fails.
- **Never permanently cache failures**: remember failures, but retry after a backoff interval; ensure a bounded number of retries.
- **De-dupe in-flight loads**: if multiple callers request the same key, share a single pending promise.

**Example pattern (lookup cache with TTL + retry-after-fail):**
```ts
const RETRY_MS = 30_000;
const TTL_MS = 60_000;

class Lookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;
  private loadedAt?: number;

  constructor(
    private readonly load: (key: string) => Promise<T>,
    private readonly onLoaded: () => void,
    private readonly now: () => number,
  ) {}

  get(key: string, refresh = false): T | undefined {
    this.start(key, refresh);
    return this.value;
  }

  async refreshNow(key: string): Promise<T | undefined> {
    await this.start(key, true);
    return this.value;
  }

  private start(key: string, refresh: boolean): Promise<void> {
    const n = this.now();
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
      this.loadedAt = undefined;
    }
    if (this.value !== undefined) {
      if (!refresh && this.loadedAt !== undefined && n - this.loadedAt < TTL_MS) {
        return Promise.resolve();
      }
      // expired: reload in background
    }
    if (this.failedAt !== undefined && n - this.failedAt < RETRY_MS) {
      return Promise.resolve();
    }
    if (this.pending) return this.pending;

    this.pending = this.load(key)
      .then((v) => {
        if (this.pending) {
          this.value = v;
          this.loadedAt = this.now();
          this.pending = undefined;
          this.failedAt = undefined;
          this.onLoaded();
        }
      })
      .catch(() => {
        if (this.pending) {
          this.failedAt = this.now();
          this.pending = undefined;
        }
      });

    return this.pending;
  }
}
```

**Application checklist for your next change**
- What is the exact semantic key for the cached result?
- What external event/revision makes the entry invalid?
- If reload fails, what state should be restored or preserved?
- Is failure retried with bounded backoff?
- Are concurrent callers sharing the same in-flight fetch?
- Does expiry trigger background refresh (no flicker)?