---
title: Cache invalidation safeguards
description: Caches must be invalidated explicitly whenever the underlying source
  of truth changes, and that invalidation must be race-safe against in-flight reads.
repository: "cline/cline\r\n"
label: Caching
language: TSX
comments_count: 6
repository_stars: 70946
---

Caches must be invalidated explicitly whenever the underlying source of truth changes, and that invalidation must be race-safe against in-flight reads.

1. Invalidate on mutation, not just on a timer. Any action that changes the cached data (a model download/delete, switching org/personal context, a file edit, a repo refresh) must actively clear or mark the relevant cache entries stale at the moment of the mutation. Don't rely on the next natural refresh to pick up the change — if a picker or view re-opens before that happens, it will show stale data (e.g. a deleted/added model missing from a list, a cached model catalog from the wrong org).

2. Guard against races between invalidation and in-flight reads. Marking something stale doesn't automatically cancel reads that are already running. Tag each cache entry/key with a generation (or version) counter that increments every time it's invalidated. When an async read resolves, check whether its generation is still current before writing the result into the cache/UI; if a newer generation has since started, discard the stale response instead of letting it clobber fresher data.

```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(key: string) {
  generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
}

async function read(key: string) {
  const generation = generationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generationRef.current.get(key) ?? 0) !== generation) {
    return; // superseded — drop this response
  }
  applyResult(key, result);
}
```

3. Avoid redundant work around invalidation. Don't cancel/restart a read that's already in flight just because the entry was marked stale — let it land, then issue a single follow-up read if the entry is still stale, rather than firing duplicate requests. Where staleness is detected by diffing a signature (e.g. counts), prefer marking "possibly stale" on any change over trying to cleverly diff equality, since content can change without the signature changing.

4. For caches that dedupe generated artifacts (e.g. writing files for repeated content), key the cache by a hash of the content itself rather than by call order, so identical data reuses the existing entry instead of accumulating duplicates. Clear such caches together with any backing storage on shutdown/exit.

Apply this pattern consistently for in-memory lists/catalogs, file/diff content caches, and any other cache sitting between the UI and a backend or external SDK.