---
title: Cache Keys And Invalidation
description: "Cache only when the cached value is provably still applicable.\n\n**Standard**\n\
  1. **Key by semantic inputs (not incidental ones)**\n   - Include *all* inputs that\
  \ change the output (e.g., tool + arguments; scope/account; repo+branch; execution\
  \ mode)."
repository: cline/cline#v1
label: Caching
language: TypeScript
comments_count: 10
repository_stars: 70862
---

Cache only when the cached value is provably still applicable.

**Standard**
1. **Key by semantic inputs (not incidental ones)**
   - Include *all* inputs that change the output (e.g., tool + arguments; scope/account; repo+branch; execution mode).
   - Normalize where order is irrelevant (e.g., object argument key order).
   - Include upstream **revision/state** when behavior can change without input-shape changes (e.g., pin revision, plugin registry status/updatedAt).

2. **Serve cached data only while the dependency still matches**
   - If the underlying definition can change (pins edited/removed, account scope switched), guard cached reads with an identity check (revision/generation/token).
   - Drop in-flight async results if the owning identity no longer matches.

3. **Invalidate before publishing dependent state**
   - When settings/scope changes affect what History/UI should show, call cache invalidation **before** posting derived state.

4. **Bound negative caching with retry backoff**
   - Cache failures (including “failed import/load”) so you don’t retry on every request.
   - Retry after a cooldown/backoff window so fixes recover automatically.

5. **Be explicit about persistence boundaries**
   - If you write recovery files used by later restore/checkpoint paths, ensure cleanup/deletion doesn’t remove data still referenced by restored sessions.

**Pattern (single-flight async lookup with retry window + identity slot)**
```ts
const RETRY_MS = 30_000;

class Lookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;

  constructor(
    private readonly now: () => number,
    private readonly onLoaded: () => void,
  ) {}

  async get(key: string, load: () => Promise<T>, refresh: boolean): Promise<T | undefined> {
    this.start(key, load, refresh);
    await this.pending; // pending exists when a (re)load is in progress
    return this.value;
  }

  private start(key: string, load: () => Promise<T>, refresh: boolean) {
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }
    if (this.value !== undefined) return;
    if (this.pending) return;
    if (this.failedAt !== undefined && this.now() - this.failedAt < RETRY_MS) return;

    const slot = {}; // identity for this attempt
    const pending = (async () => {
      try {
        const v = await load();
        if (this.pending !== pending) return; // identity guard
        this.value = v;
        this.failedAt = undefined;
        this.onLoaded();
      } catch {
        if (this.pending !== pending) return;
        this.failedAt = this.now();
      }
    })();
    this.pending = pending;
  }
}
```
Apply this across cacheable lists, derived lookups, and “load-on-demand” flows to ensure cached data never outlives its inputs, failures don’t cause loops, and restores aren’t broken by cleanup.