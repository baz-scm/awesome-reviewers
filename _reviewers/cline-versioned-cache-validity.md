---
title: Versioned cache validity
description: Cache entries must be tied to a *versioned identity* of the data and
  only served while that identity is still valid; refresh/retry must be deterministic
  and bounded.
repository: Cline/Cline
label: Caching
language: TypeScript
comments_count: 8
repository_stars: 70840
---

Cache entries must be tied to a *versioned identity* of the data and only served while that identity is still valid; refresh/retry must be deterministic and bounded.

Apply this as a coding standard:
- Build cache keys from all inputs that affect the result (scope/account id, workspace root, repo+branch, plugin set, execution mode, etc.). Include dynamic registry/status fields when they affect outcomes.
- If inputs can change while an async load is in flight, store a “slot” identifier (or revision) with the request and only commit results when the slot is still current.
- Add explicit validity checks that gate serving (e.g., “serve only while the pinned tool definition still matches the cached key”; “drop comparison baseline to the session snapshot time”). Avoid using a baseline that can be overwritten after the fact.
- Use TTL-ageout with background reload to avoid UI flicker: keep returning the cached value past TTL, but trigger an async reload; don’t let the reload spam (coalesce concurrent loads).
- For failures where fingerprint/key equality can’t detect a fix (e.g., computed/dynamic imports, invisible dependency changes), add a retry-with-backoff timer keyed to the same identity; keep retry bounded.
- For persisted recovery/cached artifacts on disk, ensure the artifact lifetime matches all consumers (including checkpoint-restored sessions). Don’t delete the source directory if restored sessions still reference files.

Example pattern (keyed cache with TTL + bounded retry):
```ts
class KeyedCache<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;
  private failedAt?: number;
  constructor(
    private readonly ttlMs: number,
    private readonly retryAfterMs: number,
    private readonly now: () => number,
  ) {}

  read(key: string, load: () => Promise<T>): T | undefined {
    this.start(key, load, false);
    return this.value;
  }

  async get(key: string, load: () => Promise<T>, refresh: boolean): Promise<T | undefined> {
    await this.start(key, load, refresh);
    return this.value;
  }

  private start(key: string, load: () => Promise<T>, refresh: boolean): Promise<void> {
    const sameKey = this.key === key;
    if (!sameKey || refresh) {
      this.key = key;
      this.value = undefined;
      this.pending = undefined;
      this.failedAt = undefined;
    }

    // Serve cached value; reload behind it on TTL expiry.
    if (this.value !== undefined && !refresh) {
      if (this.failedAt === undefined && this.now() - (this.failedAt ?? 0) < this.ttlMs) {
        return Promise.resolve();
      }
      // fallthrough: trigger reload behind
    }

    if (this.pending) return this.pending;
    if (this.failedAt !== undefined && this.now() - this.failedAt < this.retryAfterMs) {
      return Promise.resolve();
    }

    const slot = Promise.resolve();
    this.pending = slot.then(async () => {
      try {
        const v = await load();
        if (this.key === key) this.value = v;
        this.failedAt = undefined;
      } catch {
        if (this.key === key) this.failedAt = this.now();
      } finally {
        if (this.pending === slot) this.pending = undefined;
      }
    });
    return this.pending;
  }
}
```
