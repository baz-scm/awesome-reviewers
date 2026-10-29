---
title: Cache invalidation correctness
description: 'Design caches so staleness is bounded by the actual inputs that determine
  correctness, not by convenience. Two rules apply broadly:


  1. Key or invalidate every cache entry on all the inputs that can change its value
  — file modification time, a resource''s revision/state, or the exact arguments of
  a call — not just a coarse identifier or a fixed TTL. A cache...'
repository: cline/cline#1
label: Caching
language: TypeScript
comments_count: 5
repository_stars: 71024
---

Design caches so staleness is bounded by the actual inputs that determine correctness, not by convenience. Two rules apply broadly:

1. Key or invalidate every cache entry on all the inputs that can change its value — file modification time, a resource's revision/state, or the exact arguments of a call — not just a coarse identifier or a fixed TTL. A cache keyed only on a scope id or a file's existence (ignoring its content or mtime) will silently serve results computed under a configuration that no longer holds, e.g. a renamed script, an edited pin's old arguments, or a disabled plugin's stale tool list. When a TTL is genuinely necessary (e.g. a remote list that can change outside the app's control), prefer "serve stale while revalidating in the background" over either blocking reads or caching forever, and document the acceptable staleness window.

2. Never let a failed attempt to populate a cache permanently block future attempts. If a fetch/populate fails, release the in-flight handle (and avoid writing a sentinel success value) so the very next read retries instead of being stuck behind the old value or a dead promise until process restart.

Example pattern:
```ts
class Lookup<T> {
  private key?: string;
  private value?: T;
  private pending?: Promise<void>;

  async get(key: string, load: () => Promise<T>, refresh = false): Promise<T | undefined> {
    if (this.key !== key || refresh) { this.key = key; this.value = undefined; this.pending = undefined; }
    if (this.value !== undefined) return this.value;
    this.pending ??= load().then(
      (v) => { this.value = v; },
      () => { this.pending = undefined; }, // failure releases the handle so the next call retries
    );
    await this.pending;
    return this.value;
  }
}
```
Apply the same discipline to cache keys for computed/derived data: include every field that can invalidate the result (e.g. a plugin's registry `state`/`updatedAt`, a pin's tool+arguments, a file's mtime) rather than relying on a narrower key that happens to work in common cases.