---
title: Keyed caches with backoff
description: 'Any cached computation (including “warm” services and memoized lookups)
  must be correct under change, not just fast.


  **Standards**

  1. **Key caches to validity dependencies**: the cache key must include every input
  that can change the answer (e.g., pinned tool + arguments, account scope + workspace
  root + repo+branch). If key construction is tricky, encode...'
repository: cline/cline#v24
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70891
---

Any cached computation (including “warm” services and memoized lookups) must be correct under change, not just fast.

**Standards**
1. **Key caches to validity dependencies**: the cache key must include every input that can change the answer (e.g., pinned tool + arguments, account scope + workspace root + repo+branch). If key construction is tricky, encode it explicitly in one place.
2. **Guard against stale async completions**: when a request is superseded (new revision/generation/slot), discard old results. Use a per-load “slot id” (or generation check) and ignore completions that don’t match.
3. **Invalidate on boundary changes**: when scope/state changes (account switch, toggle/frontmatter authority change, session/task-history enablement), invalidate the affected caches *before* publishing new state to avoid flicker and mismatched UI.
4. **Handle failures with bounded backoff**: cache failures (or “failed-at” timestamps) and retry after a minimum delay. Never retry in a tight loop; always cap concurrency and keep UX working even if the cache is “degraded.”
5. **Only persist/copy derived state when it’s authoritative**: if another loader/source is authoritative, reconcile and retry rather than claiming cached state the loader won’t observe.

**Reusable pattern (slot-guarded lookup with failure backoff)**
```ts
const RETRY_MS = 30_000;

class SlotLookup<T> {
  private slot?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;

  read(key: string, load: () => Promise<T>, now: () => number): T | undefined {
    this.start(key, load, false, now);
    return this.value;
  }

  async get(key: string, load: () => Promise<T>, refresh: boolean, now: () => number): Promise<T | undefined> {
    await this.start(key, load, refresh, now);
    return this.value;
  }

  private start(key: string, load: () => Promise<T>, refresh: boolean, now: () => number): Promise<void> {
    const slot = `${key}`; // include all dependencies in key
    if (this.slot !== slot || refresh) {
      this.slot = slot;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }

    if (this.value !== undefined) return Promise.resolve();
    if (this.pending) return this.pending;
    if (this.failedAt !== undefined && now() - this.failedAt < RETRY_MS) return Promise.resolve();

    const current = this.pending = load().then(
      (v) => {
        if (this.pending !== current) return; // superseded
        this.value = v;
        this.pending = undefined;
      },
      () => {
        if (this.pending !== current) return; // superseded
        this.failedAt = now();
        this.pending = undefined;
      }
    );

    return current;
  }
}
```

**What to check in review**
- Is the cache key complete (all dependency inputs included)?
- Do async completions verify they still apply (generation/revision/slot guard)?
- Are caches invalidated when scope/state/authority changes?
- Are failures retried with backoff, and does the system degrade gracefully while waiting?
- Are cached/derived states consistent with the authoritative reader?