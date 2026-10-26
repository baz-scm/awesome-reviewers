---
title: Generation-Based Cache Invalidation
description: When caching async data per key, you must prevent late in-flight responses
  from overwriting newer cache contents. Use a per-key “read generation” (or similar
  token) that you bump whenever you invalidate/drop/refresh that key. Only commit
  a response if it matches the latest generation.
repository: cline/cline#v29
label: Caching
language: TSX
comments_count: 2
repository_stars: 70893
---

When caching async data per key, you must prevent late in-flight responses from overwriting newer cache contents. Use a per-key “read generation” (or similar token) that you bump whenever you invalidate/drop/refresh that key. Only commit a response if it matches the latest generation.

Also define explicit semantics for in-flight reads when an invalidation arrives:
- If a request is already loading, avoid restarting blindly.
- If the key is marked stale while loading, either keep the response and schedule exactly one follow-up read, or discard and refetch once—do so consistently to avoid fetch storms.

Finally, add deterministic tests for async cache races (hold a read open, trigger refresh/poll, then assert the late response does not replace fresh data and that exactly the expected follow-up reads occur).

Example (self-contained):
```ts
type CacheEntry<T> = { data?: T; stale?: boolean };

const cache = new Map<string, CacheEntry<string>>();
const readGeneration = new Map<string, number>();

function bumpGeneration(keys: Iterable<string>) {
  for (const k of keys) {
    readGeneration.set(k, (readGeneration.get(k) ?? 0) + 1);
  }
}

async function readKey(k: string, fetcher: () => Promise<string>) {
  const genAtStart = readGeneration.get(k) ?? 0;

  // Optionally mark stale/keep stale flag somewhere else in your state.
  const result = await fetcher();

  // Commit only if no newer generation has superseded this read.
  if ((readGeneration.get(k) ?? 0) !== genAtStart) return;

  cache.set(k, { data: result });
}

function invalidateKeys(keys: string[]) {
  // Invalidate/drop cached contents for keys.
  for (const k of keys) cache.delete(k);
  bumpGeneration(keys);

  // Decide whether to keep in-flight reads and schedule one follow-up,
  // or discard immediately—consistency matters.
}
```

Apply this pattern to any per-item cached async workflow: file trees, file contents, diff views, poll-based status, etc. The standard prevents correctness bugs caused by race conditions between refresh/poll invalidations and late async responses, and the tests ensure it stays correct as logic evolves.