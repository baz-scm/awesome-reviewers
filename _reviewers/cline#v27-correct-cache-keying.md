---
title: Correct Cache Keying
description: 'Caching must be correct under change: cache entries need complete, stable
  keys (including revisions) and must expire/revalidate safely, with bounded failure
  retry.'
repository: cline/cline#v27
label: Caching
language: TypeScript
comments_count: 7
repository_stars: 70892
---

Caching must be correct under change: cache entries need complete, stable keys (including revisions) and must expire/revalidate safely, with bounded failure retry.

Apply these rules:
1) Key by all semantic inputs (and normalize them)
- Include every input that can change the output (e.g., tool name + arguments; repository+branch; plugin discovery state).
- Normalize key order/format differences so equivalent inputs share a key.

2) Tie cached results to a correctness boundary (revision/generation)
- If the “definition” can change (pin edited, scope/account changed, session recreated), attach a revision/generation to the cache entry and only serve while it still matches.

3) Use stale-while-revalidate TTL to avoid flicker
- Serve cached data immediately while a refresh is triggered in the background once TTL/age is exceeded.

4) Cache failures briefly and retry with backoff
- Remember transient failures for a bounded window to avoid repeated expensive work.
- Retry after a fixed/backoff interval; ensure you don’t get stuck serving fallback forever—only keep fallback when refresh fails and the next user-triggered read can reattempt.

5) Make async race conditions impossible
- Use generation/scope transition guards so late async results don’t overwrite newer state.
- When comparing surfaces/diffs, take a snapshot baseline at the moment you build the related state, not a mutable field that later refreshes can overwrite.

Example pattern (stale-while-revalidate + bounded failure):
```ts
const TTL_MS = 60_000;
const FAILURE_BACKOFF_MS = 30_000;

class Lookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;

  constructor(private readonly now: () => number, private readonly load: (key: string) => Promise<T>) {}

  read(key: string): T | undefined {
    // If key changes: drop old value
    if (this.key !== key) { this.key = key; this.value = undefined; this.failedAt = undefined; }

    // Serve cached value until it expires
    const expired = this.value !== undefined && (this.now() - (this.failedAt ?? this.now())) > TTL_MS;
    if (this.value !== undefined && !expired) {
      // Trigger refresh behind the scenes only when expired/needed
      if (expired && !this.pending) void this.refresh();
      return this.value;
    }

    // If failure recently: don’t retry yet
    if (this.failedAt !== undefined && this.now() - this.failedAt < FAILURE_BACKOFF_MS) return this.value;

    void this.refresh();
    return this.value;
  }

  private async refresh() {
    if (this.pending || !this.key) return;
    const keyAtStart = this.key;
    const pending = (async () => {
      try {
        const v = await this.load(keyAtStart);
        if (this.key !== keyAtStart) return; // generation/key guard
        this.value = v;
        this.failedAt = undefined;
      } catch {
        if (this.key !== keyAtStart) return;
        this.failedAt = this.now();
      } finally {
        if (this.pending === pending) this.pending = undefined;
      }
    })();
    this.pending = pending;
    await pending;
  }
}
```