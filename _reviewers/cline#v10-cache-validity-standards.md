---
title: Cache Validity Standards
description: 'When caching derived data, ensure correctness first: make cache entries
  explicitly *valid* for the current inputs, and define what happens on changes, failures,
  and multi-source updates.'
repository: cline/cline#v10
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70869
---

When caching derived data, ensure correctness first: make cache entries explicitly *valid* for the current inputs, and define what happens on changes, failures, and multi-source updates.

Apply these rules:
1) **Tie cache entries to validity inputs**
- Key by the full input identity that affects output (e.g., tool name + normalized arguments; pin revision; plugin registry state + execution mode).
- Serve cached results only while the definition still matches; otherwise return empty/unknown or trigger a refresh.

2) **Use revisions/versions for async change detection**
- When an input can change while an async rebuild is running, attach a revision and only accept cached results for the latest revision.

3) **Make invalidation failure-safe (rollback/restore)**
- If you clear a “stale” indicator or swap caches before rebuilding, restore the stale state (or revert) when the rebuild fails so the next read retries.

4) **Use TTL/age-out + behind-the-scenes refresh to avoid flicker**
- Cache for a short TTL, but refresh asynchronously once it expires (keep rendering the old value until the new one arrives).
- Provide an explicit “force refresh” path.

5) **Handle “invisible fixes” with bounded retry/backoff**
- If fingerprinting can’t detect certain changes (e.g., dynamic imports, node_modules, side-effect-only edits), schedule re-attempts after a backoff interval, bounded to avoid loops.

6) **Multi-window/shared state: single authority + merge/prune**
- For shared records, persist an authority file/state that every window re-reads/merges from disk on refresh/write; prune entries for deleted inputs and ensure stale windows can’t incorrectly re-enable/override.

Example pattern (validity + TTL + retry skeleton):
```ts
const LOOKUP_RETRY_MS = 30_000;

class CachedLookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;

  constructor(private readonly load: (key: string) => Promise<T>,
              private readonly now: () => number) {}

  async get(key: string, refresh: boolean): Promise<T | undefined> {
    if (this.key !== key || refresh) {
      this.key = key; this.value = undefined;
      this.pending = undefined; this.failedAt = undefined;
    }
    if (this.value !== undefined) return this.value;
    if (this.pending) return undefined;
    if (this.failedAt && this.now() - this.failedAt < LOOKUP_RETRY_MS) return undefined;

    this.pending = this.load(key)
      .then(v => { if (this.pending) this.value = v; })
      .catch(() => { this.failedAt = this.now(); })
      .finally(() => { this.pending = undefined; });

    await this.pending;
    return this.value;
  }
}
```
This standard prevents serving stale/incorrect results, avoids cache invalidation races, keeps UI stable during refresh, and ensures caches recover from failures and hard-to-detect changes.