---
title: Versioned cache invalidation
description: 'When caching async-derived data, follow two rules:


  1) Don’t evict/re-fetch stable configuration on every “refresh”

  - If the underlying environment/backend is fixed for the app/session lifetime, resolve
  it once (e.g., at startup or first successful lookup) and reuse it across account
  refreshes.'
repository: cline/cline#v24
label: Caching
language: TSX
comments_count: 2
repository_stars: 70891
---

When caching async-derived data, follow two rules:

1) Don’t evict/re-fetch stable configuration on every “refresh”
- If the underlying environment/backend is fixed for the app/session lifetime, resolve it once (e.g., at startup or first successful lookup) and reuse it across account refreshes.
- Reconnect logic should only retry the *initial* lookup if it failed, not reload on every subsequent refresh.

2) If data is cached and refreshed/invalidated, make stale writes impossible
- Invalidate per key by bumping a read generation/version whenever you drop the cache (refresh, close tab, edit, etc.).
- When an async response arrives, only commit it if it matches the latest generation; otherwise discard it.
- Add a test that holds an async “read” open across an invalidation and asserts the stale response cannot overwrite the fresh contents.

Example pattern (generation guard):
```ts
type Entry<T> = { value?: T; generation: number; loading: boolean };
const cache = new Map<string, Entry<string>>();

function bumpGeneration(key: string) {
  const existing = cache.get(key);
  const nextGen = (existing?.generation ?? 0) + 1;
  cache.set(key, { ...(existing ?? { loading: false }), generation: nextGen, loading: true });
  return nextGen;
}

async function load(key: string) {
  const gen = bumpGeneration(key);
  const result = await fetchSomething(key); // async

  const current = cache.get(key);
  if (!current || current.generation !== gen) return; // discard stale response

  cache.set(key, { ...current, value: result, loading: false });
}

// Call bumpGeneration(key) on refresh/tab close/edits to invalidate.
```

This prevents both categories of bugs from the discussions: unnecessary reloads of stable config and stale async responses overwriting freshly invalidated cached data.