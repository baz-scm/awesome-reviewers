---
title: Freshness Guards for Async
description: Any async operation that can be triggered multiple times (polling, refresh,
  navigation, user actions) must not let stale/out-of-order responses overwrite newer
  state.
repository: cline/cline#v2
label: Concurrency
language: TSX
comments_count: 5
repository_stars: 70861
---

Any async operation that can be triggered multiple times (polling, refresh, navigation, user actions) must not let stale/out-of-order responses overwrite newer state.

Apply this standard:
1) Use a freshness gate for each async write.
- For per-item/per-key reads, keep a per-key requestId/generation and only apply the result if it still matches the latest value.
- For whole-component refreshes, capture a generation/requestId before each await; after every await (and before any state write), verify freshness.
2) Prevent duplicate appends/side effects with an in-flight lock.
- If multiple event paths can initiate the same async operation, route them through one guarded callback (or use a shared ref) so only one runs at a time.
3) If UI mode changes (hide/show, sign out, mode switches), bump/suspend/cleanup.
- Sign-out or mode changes should invalidate pending operations (generation bump) or temporarily suspend competing handlers.
- Ensure cleanup resets scheduler references so the next “show/arm” correctly resumes pending work.
4) When possible, remove the write race class by design.
- Store only user intent; compute derived state from current app state during render, and treat backend lookups as reads unless you can prove freshness.

Example pattern (generation gate):
```ts
const genRef = useRef(0);

async function load() {
  const gen = ++genRef.current;
  const result = await fetchSomething();
  if (gen !== genRef.current) return; // stale: do not write
  setState(result);
}

function signOut() {
  genRef.current++; // invalidate in-flight loads
  setState(/* signed-out state */);
}
```

Example pattern (per-key request id):
```ts
const requestByKeyRef = useRef(new Map<string, number>());

async function readKey(key: string) {
  const nextId = (requestByKeyRef.current.get(key) ?? 0) + 1;
  requestByKeyRef.current.set(key, nextId);

  const value = await fetchForKey(key);
  if (requestByKeyRef.current.get(key) !== nextId) return; // stale

  setCache(prev => new Map(prev).set(key, value));
}
```

Outcome: state updates become deterministic with respect to “the latest user intent,” eliminating race conditions where an older promise resolves after a newer interaction.