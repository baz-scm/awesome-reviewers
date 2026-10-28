---
title: Cache invalidation on change
description: Whenever a cache (in-memory lists, catalogs, file contents, generated
  media) can go stale due to an external event — switching accounts/orgs, a download
  or delete completing, a file being edited, or a panel refreshing — invalidate it
  explicitly at the moment that event happens rather than relying on time or incidental
  re-renders to catch it. Don't assume a...
repository: cline/cline#&&sleep 4
label: Caching
language: TSX
comments_count: 5
repository_stars: 70980
---

Whenever a cache (in-memory lists, catalogs, file contents, generated media) can go stale due to an external event — switching accounts/orgs, a download or delete completing, a file being edited, or a panel refreshing — invalidate it explicitly at the moment that event happens rather than relying on time or incidental re-renders to catch it. Don't assume a "refetch on open" is enough if the underlying trigger (e.g., org switch, pull/delete completion) can happen while the cache is still being read.

Because invalidation and in-flight reads can race (a stale request completing after a refresh/close and overwriting fresher data), tag each cache entry with a generation/version token that is bumped whenever it's invalidated, and have in-flight consumers check their token before applying results:

```ts
const readGenerationRef = useRef(new Map<string, number>());

function invalidate(keys: Iterable<string>) {
  for (const key of keys) {
    readGenerationRef.current.set(key, (readGenerationRef.current.get(key) ?? 0) + 1);
  }
}

async function readFile(path: string) {
  const generation = readGenerationRef.current.get(path) ?? 0;
  const content = await fetchContent(path);
  if ((readGenerationRef.current.get(path) ?? 0) !== generation) return; // stale, discard
  applyContent(path, content);
}
```

For data that is expensive or wasteful to recompute/rewrite (e.g., materializing identical generated files on every render), key the cache by a content hash instead of a timestamp or call count, so identical inputs reuse the same cached artifact rather than duplicating work or storage. In all cases, write a test that exercises the race (start a read, trigger invalidation, finish the read) to confirm stale data is discarded and fresh data wins.