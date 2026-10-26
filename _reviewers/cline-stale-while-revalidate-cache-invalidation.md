---
title: Stale-while-revalidate cache invalidation
description: 'When caching data fetched from an external source that can change out-of-band
  (polling, file system, git status, etc.), avoid two common pitfalls: invalidating
  based on a fragile derived signature, and clobbering fresh data with a late in-flight
  response.'
repository: cline/cline
label: Caching
language: TSX
comments_count: 3
repository_stars: 70886
---

When caching data fetched from an external source that can change out-of-band (polling, file system, git status, etc.), avoid two common pitfalls: invalidating based on a fragile derived signature, and clobbering fresh data with a late in-flight response.

- Don't key invalidation off counts or summaries that can tie (e.g. "additions:deletions"); two different changes can produce the same signature and silently skip a refresh. Instead, whenever the source snapshot changes, mark every affected cache entry `stale: true` rather than deleting it outright.
- Keep rendering the stale value while the fresh read is in flight so the UI doesn't flash a spinner on every poll; only swap in the new value once it arrives.
- Guard against races with a per-key generation counter. Bump the generation when an entry is invalidated; when a read resolves, only apply it if its generation still matches the latest. If a read is already in flight when invalidation happens, let it finish, then issue exactly one follow-up read — don't double-fetch and don't let the late response overwrite a fresher one.
- Route manual "refresh" actions through the same staleness/invalidation path as automatic polling instead of hard-clearing the cache, so there's a single, well-tested invalidation code path.
- Explicitly drop (not just mark) cache entries when their backing resource is closed/removed (e.g. closing a tab) so reopening forces a clean re-read.

Example pattern:

```ts
type Cached<T> = T & { stale?: boolean };

function markStale<T extends { stale?: boolean }>(cache: Map<string, T>) {
  const next = new Map<string, T>();
  for (const [key, entry] of cache) next.set(key, { ...entry, stale: true });
  return next;
}

const generation = new Map<string, number>();
function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    generation.set(key, (generation.get(key) ?? 0) + 1);
  }
}

async function read(key: string) {
  const gen = generation.get(key) ?? 0;
  const result = await fetchData(key);
  if ((generation.get(key) ?? 0) !== gen) {
    // stale response raced a newer invalidation — refetch once, don't apply
    return read(key);
  }
  applyResult(key, result);
}
```

Cover this behavior with a test that holds a read in flight across an invalidation/poll cycle and asserts the late response is discarded (or applied correctly) and exactly one follow-up read is issued.