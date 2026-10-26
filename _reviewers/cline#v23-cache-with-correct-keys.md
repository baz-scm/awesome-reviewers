---
title: Cache with Correct Keys
description: Cache entries must be keyed and invalidated on *every* dimension that
  can change the meaning of the cached data, and must have an aging/refresh and a
  bounded retry path so caches can’t become permanently stale.
repository: cline/cline#v23
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70889
---

Cache entries must be keyed and invalidated on *every* dimension that can change the meaning of the cached data, and must have an aging/refresh and a bounded retry path so caches can’t become permanently stale.

Apply this as a team rule:
- **Key correctness:** Include the full “scope” in the cache key (e.g., account scope, workspace identity, selected repo+branch, plugin registry state, execution mode). If a setting toggles whether data is included, **invalidate** the relevant cache before posting derived state.
- **TTL + background refresh:** When a cached read is older than a TTL, return the existing value (avoid UI flicker) but trigger a background reload; a manual refresh should force reload.
- **Negative caching limits:** Do not allow transient failures to disable functionality indefinitely. Cache “failure state” only long enough to prevent thundering herds, then **retry with backoff** (especially when changes may be invisible to your key/fingerprint).
- **Eventual consistency with bounds:** When you can’t perfectly detect changes (distributed systems, external control-plane updates, dynamic imports), add a bounded re-resolution/retry window and ensure dependent views/history are invalidated when new data arrives.

Example pattern (TTL + background refresh + bounded retries):
```ts
class Lookup<T> {
  constructor(
    private readonly now = () => Date.now(),
    private readonly ttlMs = 60_000,
    private readonly retryMs = 30_000,
    private readonly load: () => Promise<T>,
  ) {}

  private key: string | undefined;
  private value: T | undefined;
  private pending: Promise<void> | undefined;
  private loadedAt: number | undefined;
  private failedAt: number | undefined;

  read(key: string): T | undefined {
    this.start(key, false);
    return this.value;
  }

  async get(key: string, refresh = false): Promise<T | undefined> {
    await this.start(key, refresh);
    return this.value;
  }

  private async start(key: string, refresh: boolean): Promise<void> {
    if (this.key !== key || refresh) {
      this.key = key;
      this.value = undefined;
      this.loadedAt = undefined;
      this.failedAt = undefined;
      this.pending = undefined;
    }
    if (this.value !== undefined && !refresh && this.loadedAt! && this.now() - this.loadedAt! < this.ttlMs) return;
    if (this.pending) return;
    if (this.failedAt !== undefined && this.now() - this.failedAt < this.retryMs) return;

    const pending = this.load().then(
      (v) => { this.pending = undefined; this.value = v; this.loadedAt = this.now(); },
      () => { this.pending = undefined; this.failedAt = this.now(); }
    );
    this.pending = pending;
    await pending;
  }
}
```
