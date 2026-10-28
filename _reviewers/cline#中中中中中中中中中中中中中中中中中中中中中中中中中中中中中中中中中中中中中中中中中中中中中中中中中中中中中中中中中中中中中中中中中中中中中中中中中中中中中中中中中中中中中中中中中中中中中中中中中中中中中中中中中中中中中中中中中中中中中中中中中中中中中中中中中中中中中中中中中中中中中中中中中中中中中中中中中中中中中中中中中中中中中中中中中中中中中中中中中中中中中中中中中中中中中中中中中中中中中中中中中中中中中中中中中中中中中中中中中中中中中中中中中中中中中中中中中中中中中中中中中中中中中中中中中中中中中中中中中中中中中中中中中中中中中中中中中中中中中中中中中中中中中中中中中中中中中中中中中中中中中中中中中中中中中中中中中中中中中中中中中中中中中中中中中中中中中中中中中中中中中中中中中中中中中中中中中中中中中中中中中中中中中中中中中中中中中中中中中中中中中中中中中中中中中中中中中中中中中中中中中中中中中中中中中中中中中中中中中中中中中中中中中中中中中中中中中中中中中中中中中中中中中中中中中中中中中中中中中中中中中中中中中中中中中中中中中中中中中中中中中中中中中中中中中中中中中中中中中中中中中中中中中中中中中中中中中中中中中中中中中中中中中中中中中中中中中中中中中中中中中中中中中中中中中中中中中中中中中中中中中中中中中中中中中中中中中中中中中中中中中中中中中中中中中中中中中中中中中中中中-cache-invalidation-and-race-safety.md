---
title: Cache invalidation and race safety
description: Caches must be invalidated exactly when the data they represent changes,
  and must be protected against races between in-flight fetches and invalidation events.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Caching
language: TSX
comments_count: 4
repository_stars: 70984
---

Caches must be invalidated exactly when the data they represent changes, and must be protected against races between in-flight fetches and invalidation events.

1. Tie invalidation to the actual mutation, not to time or UI actions alone: when a model is downloaded or deleted, clear the relevant catalog cache; when a file/tab is closed or a repo snapshot changes, drop or mark stale the cached content for that key so the next read is fresh.

2. Guard against races with a generation/version counter per cache key. Bump the generation whenever an entry is invalidated, and tag in-flight reads with the generation they started under; when a response arrives, discard it if the generation has since changed. This prevents a slow, now-stale request from overwriting data that was already invalidated or refreshed.

Example pattern:
```ts
const readGenerationRef = useRef(new Map<string, number>());

function invalidate(key: string) {
  readGenerationRef.current.set(key, (readGenerationRef.current.get(key) ?? 0) + 1);
}

async function read(key: string) {
  const generation = readGenerationRef.current.get(key) ?? 0;
  const result = await fetchData(key);
  if (generation !== (readGenerationRef.current.get(key) ?? 0)) return; // stale, discard
  applyResult(key, result);
}
```

3. Prefer stale-while-revalidate over hard clears when the UI is involved: mark cached entries `stale` instead of deleting them so the previous value keeps rendering while a single follow-up fetch refreshes it in the background, avoiding flicker and refetch storms. Reads already in flight should be left alone; only queue a follow-up once they resolve.

4. For caches that materialize derived artifacts (e.g., writing files from repeated data), key entries by a content hash rather than by call order, so identical inputs reuse the same cached artifact instead of accumulating duplicates. Clean up cache entries together with their underlying resources (e.g., temp files) on shutdown.

Add a test that reproduces the race (e.g., hold a read open, invalidate or mark stale, then let it resolve) and asserts the stale response is dropped and exactly one follow-up read occurs.