---
title: Side-effect free cache reads
description: 'Async cache reads must not be allowed to overwrite newer state.


  Apply this standard:

  1) Guard commits with a per-key generation/request id

  - When invalidating/dropping a cache entry (refresh, tab close, edit), bump a generation
  counter for that key/path.'
repository: cline/cline#v13
label: Caching
language: TSX
comments_count: 2
repository_stars: 70874
---

Async cache reads must not be allowed to overwrite newer state.

Apply this standard:
1) Guard commits with a per-key generation/request id
- When invalidating/dropping a cache entry (refresh, tab close, edit), bump a generation counter for that key/path.
- When an async response returns, only update the cache/UI if the response’s generation matches the latest current generation.

2) Make cached reads side-effect free
- Cache/lookup logic should not perform writes that could revert the user’s latest choice.
- Keep user intent in stable, explicit state (e.g., “target/local-vs-cloud”, “selected repo”, “selected branch”), and treat async lookups as suggestions/derived reads.
- If you must write derived state from an async lookup, gate it with the same generation/current-selection checks.

Minimal pattern (generation guard):
```ts
const readGenRef = useRef(new Map<string, number>());
const bumpGen = (key: string) => {
  const next = (readGenRef.current.get(key) ?? 0) + 1;
  readGenRef.current.set(key, next);
  return next;
};

async function load(key: string) {
  const gen = bumpGen(key);
  try {
    const data = await fetchSomething(key);
    if ((readGenRef.current.get(key) ?? 0) !== gen) return; // stale
    setCache(key, data);
  } catch (e) {
    if ((readGenRef.current.get(key) ?? 0) !== gen) return; // stale
    setError(key, e);
  }
}

function refreshKey(key: string) {
  bumpGen(key); // invalidate; stale responses won’t commit
}
```

3) Test the “stale response lands after change” scenario
- Add a test that starts a read, triggers refresh/state change before it resolves, and asserts the stale response does not replace the new contents or user selection.

This prevents a common failure mode where in-flight async work completes after invalidation and corrupts the cache/UI or flips user intent.