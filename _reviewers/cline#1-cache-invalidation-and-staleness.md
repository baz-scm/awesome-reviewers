---
title: Cache invalidation and staleness
description: Whenever cached data (model catalogs, file contents, diffs, generated
  media) can be changed by an external event — a user action, a background download/delete,
  a poll, or an agent edit — the cache must be explicitly invalidated so consumers
  never read stale data. Never rely on "it will refetch eventually"; clear or mark
  the specific cache entries affected...
repository: cline/cline#1
label: Caching
language: TSX
comments_count: 8
repository_stars: 71024
---

Whenever cached data (model catalogs, file contents, diffs, generated media) can be changed by an external event — a user action, a background download/delete, a poll, or an agent edit — the cache must be explicitly invalidated so consumers never read stale data. Never rely on "it will refetch eventually"; clear or mark the specific cache entries affected as soon as the mutating event completes (e.g. clear the model-catalog cache after switching accounts or after a download/delete finishes; drop a file's cached content when its tab closes or the file is rewritten).

Because invalidation and refetching are asynchronous, guard against race conditions where an in-flight read from before the invalidation lands after a newer one and clobbers fresh data. Tag each cache entry with a generation/version counter that is bumped on invalidation, and discard any response whose generation is stale:

```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(key: string) {
  generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
}

async function read(key: string, fetcher: () => Promise<Data>) {
  const generation = (generationRef.current.get(key) ?? 0) + 1;
  generationRef.current.set(key, generation);
  const result = await fetcher();
  if (generationRef.current.get(key) !== generation) return; // superseded, drop it
  applyResult(key, result);
}
```

For UI-facing caches that are refreshed by polling or background snapshots, prefer marking entries "stale" rather than deleting them outright: keep showing the last known value and re-fetch in the background, so the UI doesn't flash a loading spinner on every poll. If a read for a key is already in flight when a new invalidation arrives, let it finish and schedule one follow-up read afterward instead of racing a second request.

Finally, when caching derived/generated artifacts (e.g. materialized files from base64 payloads), key the cache by a content hash rather than by occurrence, so identical data is reused instead of being rewritten on every access, and clean up the cache together with any backing storage on teardown.