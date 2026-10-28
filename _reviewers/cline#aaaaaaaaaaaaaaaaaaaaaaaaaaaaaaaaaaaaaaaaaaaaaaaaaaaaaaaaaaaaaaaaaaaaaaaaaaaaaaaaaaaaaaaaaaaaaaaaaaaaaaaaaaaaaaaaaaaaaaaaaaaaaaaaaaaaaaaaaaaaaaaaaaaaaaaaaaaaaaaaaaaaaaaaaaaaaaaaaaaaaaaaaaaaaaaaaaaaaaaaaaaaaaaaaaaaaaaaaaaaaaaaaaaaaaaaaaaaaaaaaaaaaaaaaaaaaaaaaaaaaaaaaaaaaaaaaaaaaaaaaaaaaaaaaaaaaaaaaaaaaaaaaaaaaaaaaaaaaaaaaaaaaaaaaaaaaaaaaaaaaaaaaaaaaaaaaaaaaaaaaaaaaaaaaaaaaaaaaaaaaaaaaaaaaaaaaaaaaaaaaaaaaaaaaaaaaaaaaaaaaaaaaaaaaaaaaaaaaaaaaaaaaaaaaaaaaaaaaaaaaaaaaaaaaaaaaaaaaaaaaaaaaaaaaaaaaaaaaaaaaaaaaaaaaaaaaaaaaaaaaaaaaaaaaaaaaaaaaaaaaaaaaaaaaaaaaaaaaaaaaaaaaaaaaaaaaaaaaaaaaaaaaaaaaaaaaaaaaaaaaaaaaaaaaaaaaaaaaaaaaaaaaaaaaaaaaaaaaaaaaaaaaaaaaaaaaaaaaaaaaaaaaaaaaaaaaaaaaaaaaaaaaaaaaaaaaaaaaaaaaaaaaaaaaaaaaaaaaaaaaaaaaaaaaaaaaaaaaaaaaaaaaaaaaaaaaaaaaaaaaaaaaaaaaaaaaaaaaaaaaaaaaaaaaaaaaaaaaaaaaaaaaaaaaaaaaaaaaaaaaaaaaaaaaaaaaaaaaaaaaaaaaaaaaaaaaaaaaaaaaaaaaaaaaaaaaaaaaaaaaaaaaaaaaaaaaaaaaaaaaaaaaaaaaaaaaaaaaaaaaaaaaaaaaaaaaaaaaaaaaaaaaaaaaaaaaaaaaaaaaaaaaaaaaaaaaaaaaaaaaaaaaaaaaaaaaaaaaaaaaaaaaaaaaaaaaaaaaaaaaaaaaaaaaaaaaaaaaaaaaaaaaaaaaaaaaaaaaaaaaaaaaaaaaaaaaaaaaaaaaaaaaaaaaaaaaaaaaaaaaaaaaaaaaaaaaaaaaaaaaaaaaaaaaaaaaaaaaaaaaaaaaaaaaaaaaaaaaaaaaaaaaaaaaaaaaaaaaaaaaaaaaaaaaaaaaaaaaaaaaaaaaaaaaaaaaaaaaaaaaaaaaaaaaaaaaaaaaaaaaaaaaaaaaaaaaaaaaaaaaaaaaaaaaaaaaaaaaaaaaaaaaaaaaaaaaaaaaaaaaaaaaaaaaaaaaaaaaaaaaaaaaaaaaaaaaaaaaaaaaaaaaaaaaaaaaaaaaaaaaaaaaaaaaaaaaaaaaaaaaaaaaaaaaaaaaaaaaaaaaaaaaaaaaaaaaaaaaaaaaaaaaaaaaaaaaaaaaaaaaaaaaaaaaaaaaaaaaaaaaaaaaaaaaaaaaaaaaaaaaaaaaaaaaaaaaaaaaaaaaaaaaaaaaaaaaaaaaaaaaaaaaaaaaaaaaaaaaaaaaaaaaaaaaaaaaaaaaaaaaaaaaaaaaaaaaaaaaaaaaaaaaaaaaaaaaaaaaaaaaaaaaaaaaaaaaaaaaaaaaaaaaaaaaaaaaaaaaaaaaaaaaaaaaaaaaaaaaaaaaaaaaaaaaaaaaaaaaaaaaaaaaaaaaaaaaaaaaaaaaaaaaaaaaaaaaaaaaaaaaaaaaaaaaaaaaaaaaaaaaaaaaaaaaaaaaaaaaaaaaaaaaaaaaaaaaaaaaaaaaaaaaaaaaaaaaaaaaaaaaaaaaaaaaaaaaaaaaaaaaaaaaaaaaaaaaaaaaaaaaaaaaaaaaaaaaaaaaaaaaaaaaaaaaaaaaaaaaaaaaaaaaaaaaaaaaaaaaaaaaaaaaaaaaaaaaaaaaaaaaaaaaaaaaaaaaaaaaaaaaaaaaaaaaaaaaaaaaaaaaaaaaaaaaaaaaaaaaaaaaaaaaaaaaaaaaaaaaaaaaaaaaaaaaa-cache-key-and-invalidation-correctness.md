---
title: Cache key and invalidation correctness
description: 'Caches must stay correct as the underlying data changes, not just fast.
  When adding or reviewing a cache:


  1. **Key on everything that affects the value.** If a result depends on more than
  just the lookup id, include those inputs in the key (or revalidate against them).
  Example: a pinned-read cache keyed only by scope id served stale results after a
  pin''s...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Caching
language: TypeScript
comments_count: 9
repository_stars: 70967
---

Caches must stay correct as the underlying data changes, not just fast. When adding or reviewing a cache:

1. **Key on everything that affects the value.** If a result depends on more than just the lookup id, include those inputs in the key (or revalidate against them). Example: a pinned-read cache keyed only by scope id served stale results after a pin's tool/arguments changed — the fix added a revision to the key. A plugin-tool-inspection cache missed that a plugin's registry state (enabled/disabled, reloaded) also determines the result, so it kept serving tools for a plugin the session had turned off. A warmed sidecar service cache was keyed by the wrong path (process cwd instead of the resolved workspace), warming an entry nothing would ever read.

2. **Don't let a retained connection or past success stand in for a fresh check.** A long-lived host/connection is not proof the cached state is still valid — revalidate settled/cached status against the latest source record on each use, the same check applied on restart, rather than trusting "we're still connected" as永久 confirmation.

3. **Never cache a failed or partial result as if it succeeded.** Only cache clean/complete outcomes; a failed fetch should release its cache slot so the next read retries, instead of pinning a fallback value or an error state indefinitely. Equally, don't act on a cache as if it was populated when the fill failed (e.g., skip a "cache updated" notification if the fetch didn't actually fill it).

4. **Use TTL / stale-while-revalidate deliberately, not as the only invalidation signal.** Time-based expiry is fine for data whose source can't push invalidation (e.g., external repo permissions): serve the last known value immediately, refresh in the background, and still offer an explicit manual-refresh path. But where the source can tell you something changed, prefer that signal over waiting out a TTL.

5. **Bound cache size and lifetime, and account for every field you compare.** Enforce eviction (LRU/size/TTL) and verify every branch that extracts bytes/content for budget or eviction decisions covers all real-world shapes (e.g., an eviction-size check must handle both `mediaType` and `mimeType` image fields, or large content silently evades the budget). If a cache writes to disk, write once and give it a disposal/cleanup path — don't rewrite/re-truncate on every read and don't leak files that are never deleted.

```ts
// Key must capture every dimension that determines validity.
const cacheKey = `${pin.id}:${hash(pin.tool, pin.arguments)}`;

// Don't cache a failed fill.
try {
  const value = await fetch();
  cache.set(key, value); // only on success
} catch {
  cache.delete(key); // let the next read retry
}
```

Before merging a cache, ask: what inputs determine this value, does every one of them participate in invalidation, and what happens on a failed fill?