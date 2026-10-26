---
title: Correct Cache Invalidation
description: 'Caches must be correct under async updates: key entries with all inputs
  that affect the result, tie cached value acceptance to a version/revision snapshot,
  and use explicit TTL + stale-while-revalidate + failure backoff.'
repository: cline/cline#v2
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70861
---

Caches must be correct under async updates: key entries with all inputs that affect the result, tie cached value acceptance to a version/revision snapshot, and use explicit TTL + stale-while-revalidate + failure backoff.

Apply these rules:
- Key completeness: include every dependency that can change output (e.g., tool identity + arguments, plugin execution mode + discovery state, account scope).
- Version/revision gating: when launching async loads/refreshes, capture a “revision” and only commit results if the current revision still matches. This prevents late replies from older definitions from overwriting newer truth.
- Baseline snapshots: when comparing/diffing (e.g., session recovery), store the baseline at the moment you build the session/surface; don’t diff against a later, unrelated cache snapshot.
- TTL semantics: prefer stale-while-revalidate when UX matters (return cached value until TTL expiry threshold; reload behind the scenes to avoid flicker). Make Refresh force a synchronous reload.
- Failure caching: on transient failures, remember failure with a timestamp and retry after a backoff window (prevents indefinite feature disabling and prevents repeated expensive attempts).
- Persistence durability: if later steps (checkpoint/restore/resume) depend on files/paths, never destructively rewrite or truncate them in a way that breaks restoration.

Sketch pattern (stale-while-revalidate + revision gating):
```ts
type Entry<T> = {
  value: T | undefined;
  expiresAt: number;          // TTL for freshness
  failedAt: number | undefined;
  pending?: Promise<void>;  // in-flight refresh
  revision: number;          // increments when inputs/deps change
};

class SafeCache<T> {
  private entry: Entry<T> = { value: undefined, expiresAt: 0, failedAt: undefined, revision: 0 };
  private revision = 0;

  invalidate() { this.revision++; this.entry = { ...this.entry, value: undefined, pending: undefined, failedAt: undefined, revision: this.revision }; }

  getStaleWhileRevalidate(load: () => Promise<T>, now = Date.now(), ttlMs: number, retryMs: number): T | undefined {
    const { value, expiresAt, failedAt, pending, revision } = this.entry;

    // Serve stale (or empty) but schedule refresh when needed.
    const stale = now >= expiresAt;
    const canRetry = failedAt === undefined || now - failedAt >= retryMs;
    if (stale && !pending && canRetry) {
      const myRevision = this.revision;
      const refresh = load().then(
        (v) => {
          // Accept only if nothing changed while we awaited.
          if (this.revision !== myRevision) return;
          this.entry.value = v;
          this.entry.expiresAt = now + ttlMs;
          this.entry.failedAt = undefined;
        },
        () => {
          if (this.revision !== myRevision) return;
          this.entry.failedAt = now;
        }
      ).finally(() => {
        if (this.revision === revision) this.entry.pending = undefined;
      });
      this.entry.pending = refresh;
    }
    return value;
  }
}
```
Use this standard to prevent stale/late async results, ensure cache invalidation when dependencies change, and keep refresh behavior predictable across distributed/session flows.