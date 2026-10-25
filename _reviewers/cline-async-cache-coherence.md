---
title: Async cache coherence
description: When caching data that arrives asynchronously (API/desktop invokes, polling,
  or snapshot-driven loads), make cache coherence explicit so late/stale responses
  can’t overwrite fresher state.
repository: cline/CLINE
label: Caching
language: TSX
comments_count: 3
repository_stars: 70839
---

When caching data that arrives asynchronously (API/desktop invokes, polling, or snapshot-driven loads), make cache coherence explicit so late/stale responses can’t overwrite fresher state.

Apply these rules:
1) Version per cache key (generation/token)
- Keep a per-key “generation” counter in a ref/state.
- Increment the generation whenever you drop/refresh that key’s cached entry (refresh, tab close, edits).
- When a response returns, only commit it if it still matches the generation.

2) Handle in-flight reads deterministically
- If a key’s snapshot says it’s stale while a read is already in flight, don’t blindly cancel.
- Either: (a) keep the in-flight response but schedule exactly one follow-up re-read after it finishes, or (b) discard it and start a fresh read—choose one policy and test it.

3) Unify refresh paths
- Don’t treat “manual refresh” differently from snapshot/poll invalidation; route it through the same invalidation + generation logic.

4) Cache stable configuration with correct lifecycle scope
- If a value is stable for the app/environment lifetime, resolve it once (and retry only when initial lookup fails), rather than re-fetching on every account refresh/reconnect.

Minimal pattern (per-key generation + discard late writes):

```ts
const readGenRef = useRef(new Map<string, number>());
const invalidateReads = (keys: Iterable<string>) => {
  for (const key of keys) {
    readGenRef.current.set(key, (readGenRef.current.get(key) ?? 0) + 1);
  }
};

async function readKey(key: string) {
  const gen = readGenRef.current.get(key) ?? 0;
  const result = await fetchSomethingFor(key);
  if ((readGenRef.current.get(key) ?? 0) !== gen) return; // discard stale
  setCacheFor(key, result);
}
```

Also add tests that reproduce the failure mode: keep a read in flight, trigger refresh/invalidation, then ensure the late response does not overwrite the fresh contents and that any required follow-up read happens exactly once.