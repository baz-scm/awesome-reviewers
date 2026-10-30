---
title: Cache invalidation guarantees
description: 'Any in-memory cache (model catalogs, file/diff contents, media files,
  lists) must be explicitly invalidated whenever the data it holds can go stale: switching
  accounts/orgs, completing a mutation (download, delete, discard, commit), an agent
  edit, or a manual refresh. Simply clearing a cache on refresh is not enough if async
  reads are in flight — a slow...'
repository: cline/cline#"><b>zze3729958
label: Caching
language: TSX
comments_count: 8
repository_stars: 71067
---

Any in-memory cache (model catalogs, file/diff contents, media files, lists) must be explicitly invalidated whenever the data it holds can go stale: switching accounts/orgs, completing a mutation (download, delete, discard, commit), an agent edit, or a manual refresh. Simply clearing a cache on refresh is not enough if async reads are in flight — a slow response that started before invalidation can land after and silently overwrite fresher data. Guard against this by tagging each cache entry with a generation/version number that is bumped on invalidation; before applying a response, check it still matches the current generation for that key, and discard it otherwise.

Prefer marking entries as "stale" rather than deleting them outright, then triggering a background re-read while still rendering the stale value — this avoids flashing a loading spinner on every poll or refresh. Skip re-fetching a key that is already loading; instead, let the in-flight read finish and, if the entry was marked stale meanwhile, issue one follow-up read afterward rather than many duplicate requests. When caching derived/generated content (e.g., hashed media), key the cache by a content hash so identical inputs reuse the same cached artifact instead of duplicating storage.

Example pattern for per-key invalidation with races:
```ts
const generationRef = useRef(new Map<string, number>());

function invalidate(key: string) {
  generationRef.current.set(key, (generationRef.current.get(key) ?? 0) + 1);
}

async function read(key: string) {
  const generation = (generationRef.current.get(key) ?? 0) + 1;
  generationRef.current.set(key, generation);
  const isCurrent = () => generationRef.current.get(key) === generation;
  const result = await fetchData(key);
  if (!isCurrent()) return; // a newer invalidation/read superseded this one
  applyResult(key, result);
}
```
Apply this pattern consistently for any cache tied to async fetches so that account switches, deletions, edits, and concurrent refreshes cannot leave the UI or backend showing outdated or duplicated data.