---
title: Cache invalidation correctness
description: 'Caches must stay correct as the underlying data changes, not just fast.
  When designing a cache:


  1. **Key on everything that affects the value.** A cache key must encode every input
  that can change the result (e.g. include a plugin''s registry state/`updatedAt`
  and execution mode in an inspection cache key), otherwise a changed input (a plugin
  turned off, a...'
repository: cline/cline#"><b>zze3729958
label: Caching
language: TypeScript
comments_count: 5
repository_stars: 71067
---

Caches must stay correct as the underlying data changes, not just fast. When designing a cache:

1. **Key on everything that affects the value.** A cache key must encode every input that can change the result (e.g. include a plugin's registry state/`updatedAt` and execution mode in an inspection cache key), otherwise a changed input (a plugin turned off, a config flipped) returns a stale answer under the old key.

2. **Invalidate explicitly on every mutation that affects cached data**, don't rely solely on TTL. When a setting like `cloudSessionsEnabled` changes, call the corresponding `invalidateCache()` before the next read so the next listing re-enumerates with the new state.

3. **Never treat a retained connection/resource as permanent proof of freshness.** A value learned once (e.g. a remembered status) must be revalidated against the source's own version/timestamp on each use; a retained socket or handle is not evidence that nothing changed elsewhere. Re-check the source record version and fall back to "unconfirmed" when it has moved on.

4. **Don't cache failures.** Only persist a cache entry for a clean/successful computation; a failed attempt must leave the cache empty (or mark it explicitly failed) so the very next read retries rather than being stuck replaying the failure or stale fallback. Release any "warm-up"/in-flight handle on failure so a later caller re-triggers the fetch.

5. **Use TTL with background refresh (stale-while-revalidate) for latency-sensitive reads.** Serve the cached value immediately to avoid UI flicker, but kick off a reload once the entry ages past its TTL so externally-changed state (e.g. access granted/revoked remotely) surfaces on the next read without blocking the current one. Pair this with an explicit "force refresh" affordance for users who need up-to-date data immediately.

Example pattern:
```ts
async get(key: string, load: () => Promise<T>, refresh: boolean): Promise<T | undefined> {
  if (this.key !== key || refresh) { this.key = key; this.value = undefined; this.failedAt = undefined }
  if (this.value !== undefined) return this.value
  if (this.failedAt !== undefined && this.now() - this.failedAt < RETRY_MS) return undefined
  try {
    this.value = await load()
  } catch {
    this.failedAt = this.now() // don't cache the failure itself; allow retry after backoff
  }
  return this.value
}
```

Applying these rules prevents the two most common cache bugs: serving a value that is provably stale because the key or invalidation missed an input, and getting stuck on a cached failure that should have retried.</description>
</RawReviewerOutputSchema>

