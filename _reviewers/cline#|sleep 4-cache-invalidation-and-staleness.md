---
title: Cache invalidation and staleness
description: 'When caching derived or remote data, invalidate deliberately and safely
  rather than relying on cheap heuristics:


  1. **Key caches by content identity when deduping.** For example, cache generated
  media by a hash of its type+bytes so re-processing identical content reuses the
  existing entry instead of writing duplicates (e.g. `materializeGeneratedMedia`...'
repository: cline/cline#|sleep 4
label: Caching
language: TSX
comments_count: 5
repository_stars: 70979
---

When caching derived or remote data, invalidate deliberately and safely rather than relying on cheap heuristics:

1. **Key caches by content identity when deduping.** For example, cache generated media by a hash of its type+bytes so re-processing identical content reuses the existing entry instead of writing duplicates (e.g. `materializeGeneratedMedia` caching by content hash, cleared on process exit).

2. **Invalidate explicitly when the source of truth changes**, not implicitly. If an action (install, delete, upload) changes backend state that a cache mirrors, clear or refresh that specific cache entry right after the action (e.g. clearing a models-catalog cache after a pull/delete completes), and do the same when a UI element that owns a cache entry closes (e.g. drop a file/diff cache when its tab closes) so the next read is guaranteed fresh.

3. **Avoid signature/count-based staleness checks that can miss real changes.** Comparing counts or simple digests can pass even when content changed. Prefer marking all potentially-affected entries `stale` on any new snapshot/state update, rather than trying to diff for exact changes.

4. **Keep serving stale data while revalidating** to avoid UI flicker — don't clear the cache outright; mark entries stale, keep rendering the last good value, and trigger a background refetch.

5. **Guard against races between in-flight reads and invalidation.** Use a per-key generation/version counter that increments on invalidation; a response for a key is only applied if its generation still matches, and if a read was invalidated while in flight, let it apply once if marked merely "stale" but trigger exactly one follow-up read afterward.

Example pattern:
```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
  }
}

async function read(key: string) {
  const generation = generationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if (generationRef.current.get(key) !== generation) {
    // superseded while in flight — drop or trigger one follow-up read
    return;
  }
  applyResult(key, result);
}
```

Applying this consistently prevents stale UI, duplicate files/entries, flicker from over-aggressive clearing, and race conditions where an outdated response overwrites a newer one.