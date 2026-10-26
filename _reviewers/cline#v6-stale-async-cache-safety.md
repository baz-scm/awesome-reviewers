---
title: Stale Async Cache Safety
description: 'When using cached data with async fetches, ensure that late/stale responses
  can’t overwrite newer cache entries or user intent.


  Apply these rules:

  1) Version per cache key (generation/version counters)'
repository: cline/cline#v6
label: Caching
language: TSX
comments_count: 3
repository_stars: 70864
---

When using cached data with async fetches, ensure that late/stale responses can’t overwrite newer cache entries or user intent.

Apply these rules:
1) Version per cache key (generation/version counters)
- On invalidation (refresh/tab close/edit), bump a generation/read-id for that key.
- When an async response arrives, apply it only if it still matches the latest generation.

Example pattern:
```ts
const readGen = useRef(new Map<string, number>());
function bump(key: string) {
  readGen.current.set(key, (readGen.current.get(key) ?? 0) + 1);
}
async function load(key: string, fetchFn: () => Promise<string>) {
  bump(key);
  const gen = readGen.current.get(key)!;
  const data = await fetchFn();
  if (readGen.current.get(key) !== gen) return; // discard stale response
  setStateForKey(key, data);
}
```

2) Don’t let derived async lookups overwrite user-controlled selections
- Store “intent” (e.g., Local vs Cloud) separately from “derived data” (e.g., repo/branch suggestions).
- Update only derived fields after lookups; never let a late lookup flip an already-changed selection.

3) Resolve stable configuration once
- If backend/environment/app-target configuration is fixed for the session lifetime, fetch/resolve it once at startup.
- Retries on reconnect should cover only the initial failure (not reloading on unrelated refreshes).

4) Add tests that force out-of-order completion
- Hold an in-flight read open, trigger a refresh/invalidation, then resolve the stale read and assert it does not replace fresh state.

These practices prevent the common caching failure mode: out-of-order async results corrupting current state.