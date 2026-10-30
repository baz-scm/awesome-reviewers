---
title: Cache invalidation and lifecycle
description: 'Every cache must have an explicit, correct trigger for invalidation
  and a bounded lifecycle — don''t just set-and-forget a value.


  1. Key cache entries by what actually determines validity, not just an id. A pinned
  tool result should be keyed by the tool+arguments it was computed from so an edited
  or removed pin can never serve the old value; a...'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 71067
---

Every cache must have an explicit, correct trigger for invalidation and a bounded lifecycle — don't just set-and-forget a value.

1. Key cache entries by what actually determines validity, not just an id. A pinned tool result should be keyed by the tool+arguments it was computed from so an edited or removed pin can never serve the old value; a scope/account-bound cache must be keyed by that scope so switching accounts never leaks stale data.
2. Define the real invalidation trigger. When a setting or toggle changes behavior that a cache depends on (e.g. `cloudSessionsEnabled` affecting task history), invalidate that cache as part of the same write, not on the next unrelated refresh.
3. Never leave a cache "stuck" after a failed population. If a background warm-up or refresh fails without filling the cache, release the in-flight/pending marker so the next read retries instead of silently keeping the fallback forever.
4. Prefer stale-while-revalidate over hard blocking: serve the last known-good value immediately past its TTL while reloading in the background, rather than blocking or flickering empty — but document the acceptable staleness window, especially for externally-mutable data (e.g. repo access granted/revoked elsewhere) where some lag is an accepted, inherent limitation of distributed state.
5. Get eviction logic right and tested. Budget/size-based eviction (LRU, byte caps) must correctly classify all variants of the data it accounts for (e.g. check every schema's media-type field, not just one convention), or large items can bypass accounting and evict otherwise-recoverable entries.
6. Any cache or store backed by disk or other external resources needs a disposal/cleanup path and should write once rather than rewriting/re-truncating on every subsequent read — persistent "caches" without eviction are leaks, not caches.

Example pattern for safe population with retry-on-failure:
```ts
private pending: Promise<void> | undefined;
private start(key: string, load: () => Promise<T>): Promise<void> {
  if (this.pending) return this.pending;
  const p = load().then(
    (value) => { this.value = value; this.pending = undefined; },
    () => { this.pending = undefined; }, // release on failure so retry can happen
  );
  this.pending = p;
  return p;
}
```