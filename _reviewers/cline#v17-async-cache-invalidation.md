---
title: Async cache invalidation
description: When caching async data (per file/path/query), assume responses can arrive
  out of order. Always prevent “stale in-flight” results from overwriting fresher
  cache state, and unify invalidation/refresh paths.
repository: cline/cline#v17
label: Caching
language: TSX
comments_count: 3
repository_stars: 70883
---

When caching async data (per file/path/query), assume responses can arrive out of order. Always prevent “stale in-flight” results from overwriting fresher cache state, and unify invalidation/refresh paths.

Rules:
1) Generation-per-key: maintain a monotonically increasing token per cache key. Bump it whenever you drop/refresh that key.
2) Verify before commit: capture the token when starting a read; only write the response if the token still matches.
3) Snapshot/stale handling: if new invalidation happens while a read is already in flight, either mark it stale and schedule exactly one follow-up read, or keep the current response but ensure a re-read occurs after completion.
4) Cache lifetime: cache stable configuration (e.g., environment/base URL) once at startup; don’t reload it on unrelated account refresh/reconnect events.

Example pattern:
```ts
const genRef = useRef(new Map<string, number>());

function bump(keys: Iterable<string>) {
  for (const k of keys) genRef.current.set(k, (genRef.current.get(k) ?? 0) + 1);
}

async function readAndCache(key: string) {
  const genAtStart = genRef.current.get(key) ?? 0;
  setCache(k, { loading: true });

  const result = await fetchForKey(key);

  // Discard if invalidated since the read started
  if ((genRef.current.get(key) ?? 0) !== genAtStart) return;

  setCache(key, { data: result, loading: false });
}
```

Also add tests that simulate polling/in-flight reads across invalidation to ensure stale responses can’t replace fresh cache entries.