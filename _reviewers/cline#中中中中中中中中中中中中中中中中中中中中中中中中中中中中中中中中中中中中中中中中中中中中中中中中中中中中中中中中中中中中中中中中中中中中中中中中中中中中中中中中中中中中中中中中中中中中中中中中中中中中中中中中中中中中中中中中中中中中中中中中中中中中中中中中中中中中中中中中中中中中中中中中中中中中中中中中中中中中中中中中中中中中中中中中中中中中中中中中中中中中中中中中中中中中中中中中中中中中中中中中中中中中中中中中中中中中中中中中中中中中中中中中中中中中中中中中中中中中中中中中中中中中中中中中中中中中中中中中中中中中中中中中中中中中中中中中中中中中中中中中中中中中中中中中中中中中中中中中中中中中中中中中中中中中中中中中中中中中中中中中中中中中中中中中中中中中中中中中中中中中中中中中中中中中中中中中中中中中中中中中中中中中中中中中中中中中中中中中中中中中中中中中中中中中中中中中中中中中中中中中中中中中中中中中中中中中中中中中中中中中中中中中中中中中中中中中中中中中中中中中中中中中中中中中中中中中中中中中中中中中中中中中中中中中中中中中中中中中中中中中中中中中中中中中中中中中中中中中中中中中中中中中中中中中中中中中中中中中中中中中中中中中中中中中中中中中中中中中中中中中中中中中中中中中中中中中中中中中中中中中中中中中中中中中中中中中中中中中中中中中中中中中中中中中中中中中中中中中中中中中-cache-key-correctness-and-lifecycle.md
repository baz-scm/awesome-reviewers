---
title: Cache key correctness and lifecycle
description: 'A cached value is only as safe as the key and lifecycle around it. When
  adding or reusing a cache:


  1. **Key on everything that affects validity, not just the obvious identity.** If
  any input that could change the cached result (a revision, config state, enabled/disabled
  flag, execution mode, account scope, or resolved path) is left out of the key, callers...'
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Caching
language: TypeScript
comments_count: 5
repository_stars: 70984
---

A cached value is only as safe as the key and lifecycle around it. When adding or reusing a cache:

1. **Key on everything that affects validity, not just the obvious identity.** If any input that could change the cached result (a revision, config state, enabled/disabled flag, execution mode, account scope, or resolved path) is left out of the key, callers will silently get stale or cross-context data. Example: a pinned-read cache keyed only by scope id served results from an edited/removed pin; fixing it meant keying by `tool + arguments` and tagging scopes with a revision so an edit invalidates immediately instead of waiting out the TTL. Similarly, a plugin-inspection cache must key on the plugin's registry `state`/`updatedAt`, not just file fingerprints, so a plugin toggled off/on forces a fresh read. When a warm-up and its consumer compute the cache key independently (e.g. from workspace path), make sure they resolve the identical value — a warm-up using a different cwd than the chat session warms the wrong key and does nothing useful.

2. **Never cache a failed or partial result as if it were valid.** A failure may be fixed by something outside the cache's fingerprint (e.g. installing a missing dependency), so only successful/complete computations should be written to the cache; failed attempts should be retried on the next read, not frozen in place.

3. **Make TTL and refresh behavior explicit.** Prefer stale-while-revalidate for read-heavy caches: return the last good value immediately and refresh in the background, so staleness is bounded without blocking the caller or causing UI flicker. Provide an explicit force-refresh path for user-triggered updates.

4. **Give every cache a disposal/cleanup path**, especially when it is backed by external resources (disk files, sockets, sandboxes). A cache or store with no dispose path accumulates unbounded garbage across runs; define when entries are evicted (size/LRU/idle-based) and when backing resources are deleted.

5. **Only mutate cache-driven side effects (e.g. re-posting UI state) when the cache was actually updated.** A background refresh that fails and falls back to a default must not trigger the same side effect as a successful refresh, or callers can loop indefinitely on a no-op.