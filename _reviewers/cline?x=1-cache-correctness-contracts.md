---
title: Cache Correctness Contracts
description: 'When caching results in an async/distributed plugin environment, make
  cache correctness explicit:


  - **Key by semantics, not by convenience:** include every input that changes meaning
  (e.g., pinned tool+arguments, selected revision, plugin registry status, account
  scope).'
repository: cline/cline?x=1
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70861
---

When caching results in an async/distributed plugin environment, make cache correctness explicit:

- **Key by semantics, not by convenience:** include every input that changes meaning (e.g., pinned tool+arguments, selected revision, plugin registry status, account scope).
- **Version everything user-facing:** for “sets” shown in UI, attach a **revision** (or equivalent) and reject actions from stale revisions.
- **Stale-guard async writes:** never let late responses update current state unless the cache key/revision still matches.
- **Use TTL and bounded backoff:** refresh list/lookup data after a TTL; failed loads should retry on a time backoff (not forever, not on every call).
- **Invalidate on true state boundaries:** invalidate derived projections (e.g., history) on scope transitions and real changes, and avoid cross-scope/account bleed.
- **Persist with deterministic ownership:** if multiple windows/processes can update shared authority, merge deterministically and prune entries for deleted/unknown keys.

Example pattern (keyed cache with dedupe + failed-at backoff):
```ts
const LOOKUP_RETRY_MS = 30_000;
class Lookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;
  constructor(private readonly now: () => number, private readonly onLoaded: () => void) {}

  get(key: string, load: () => Promise<T>, refresh: boolean): Promise<T | undefined> {
    return this.start(key, load, refresh).then(() => this.value);
  }

  private start(key: string, load: () => Promise<T>, refresh: boolean): Promise<void> {
    if (this.key !== key || refresh) {
      this.key = key; this.value = undefined; this.pending = undefined; this.failedAt = undefined;
    }
    if (this.value !== undefined) return Promise.resolve();
    if (this.pending) return this.pending;
    if (this.failedAt !== undefined && this.now() - this.failedAt < LOOKUP_RETRY_MS) {
      return Promise.resolve();
    }
    const pending = load().then(v => {
      if (this.pending !== pending) return;
      this.pending = undefined; this.value = v; this.onLoaded();
    }).catch(() => {
      if (this.pending !== pending) return;
      this.pending = undefined; this.failedAt = this.now();
    });
    this.pending = pending;
    return pending;
  }
}
```
Apply this pattern to: pinned read results, cloud session lookups, plugin tool discovery/import retries, and any UI set that must not accept stale actions.