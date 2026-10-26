---
title: Async cache invalidation
description: 'Ensure cached/derived data updates are race-safe and lifecycle-correct:
  when you invalidate a cache entry, inflight async reads must not overwrite newer
  data; and for values that are stable for the app/session lifetime, resolve them
  once rather than reloading on unrelated refreshes.'
repository: cline/cline#v4
label: Caching
language: TSX
comments_count: 2
repository_stars: 70864
---

Ensure cached/derived data updates are race-safe and lifecycle-correct: when you invalidate a cache entry, inflight async reads must not overwrite newer data; and for values that are stable for the app/session lifetime, resolve them once rather than reloading on unrelated refreshes.

Apply two rules:

1) Race-safe invalidation with a generation token
- Maintain a per-key “generation/readId” for cached content.
- Increment (or bump) the generation whenever you drop/refresh that cache entry.
- When an async request returns, only apply it if it matches the latest generation for that key.
- Add a test where a read stays open across a refresh and confirm stale responses never replace fresh state.

Example pattern:
```ts
const generations = new Map<string, number>();

function bumpGeneration(key: string) {
  const next = (generations.get(key) ?? 0) + 1;
  generations.set(key, next);
  return next;
}

async function loadCached(key: string, fetcher: () => Promise<string>, apply: (v: string) => void) {
  const gen = generations.get(key) ?? 0; // capture current generation
  const value = await fetcher();

  // Only commit if still current
  if ((generations.get(key) ?? 0) !== gen) return;
  apply(value);
}

function refreshKey(key: string, fetcher: () => Promise<string>, apply: (v: string) => void) {
  bumpGeneration(key); // invalidation happens first
  void loadCached(key, fetcher, apply);
}
```

2) Don’t reload stable config on every refresh
- If a value is “fixed for the app’s lifetime” (e.g., a resolved base URL tied to the backend/environment at startup), fetch it once at startup.
- On reconnect, retry only if the initial lookup failed; don’t re-resolve on unrelated refreshes.

This prevents stale async responses from reintroducing invalid cached data, and avoids unnecessary cache churn/reloads that can cause UI flicker or wasted work.