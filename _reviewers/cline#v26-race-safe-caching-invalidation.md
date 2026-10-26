---
title: Race-safe caching invalidation
description: 'Cache should match the real lifetime of the underlying value, and async
  cached reads must be invalidated without race conditions.


  Apply these rules:

  1) Resolve and cache stable configuration once'
repository: cline/cline#v26
label: Caching
language: TSX
comments_count: 2
repository_stars: 70893
---

Cache should match the real lifetime of the underlying value, and async cached reads must be invalidated without race conditions.

Apply these rules:
1) Resolve and cache stable configuration once
- If the backend/environment is effectively fixed for the app lifetime, fetch it once at startup and reuse it across user/account refreshes and reconnects.
- Avoid reloading stable “configuration-like” values inside frequently-called refresh paths.

2) For cached async results, invalidate by “staling,” not by clobbering
- When new snapshots/polls arrive, mark existing cache entries as `stale` so the UI can re-render the “current view” while ensuring a refresh occurs.
- Do not drop responses already in-flight; instead:
  - If an in-flight read completes, keep it only if it’s still the latest generation.
  - If it was marked stale by a later snapshot, schedule exactly one follow-up read.
- Use a per-key generation counter (or similar token) so late responses can’t overwrite fresher data.

Example pattern (self-contained):
```ts
const generation = new Map<string, number>();
const invalidate = (keys: Iterable<string>) => {
  for (const k of keys) generation.set(k, (generation.get(k) ?? 0) + 1);
};

const read = async (key: string, fetcher: () => Promise<string>) => {
  const gen = generation.get(key) ?? 0;
  const result = await fetcher();
  // Only apply if this response matches the latest invalidation generation.
  if ((generation.get(key) ?? 0) !== gen) return;
  return result;
};
```

This prevents unnecessary re-fetching for stable values and ensures cached async data stays correct under polling, reconnection, and StrictMode-style re-render behavior.