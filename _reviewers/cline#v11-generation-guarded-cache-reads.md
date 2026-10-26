---
title: Generation-guarded cache reads
description: When caching data that is populated via async requests, make cache lifetime
  explicit and prevent out-of-order responses from overwriting newer cache/state.
repository: cline/cline#v11
label: Caching
language: TSX
comments_count: 2
repository_stars: 70871
---

When caching data that is populated via async requests, make cache lifetime explicit and prevent out-of-order responses from overwriting newer cache/state.

1) Guard cache updates with a per-key generation/token
- For each cache entry (e.g., “path” or “resource id”), maintain a monotonically increasing generation/read token.
- Increment/bump the generation whenever you invalidate/drop the cache entry (refresh, tab close, explicit “clear”, etc.).
- Capture the generation when starting the async request; when it resolves, only apply the result if the generation still matches. Otherwise discard the stale response.
- Add a test that triggers a refresh/invalidation while a read is in-flight and asserts the stale response cannot replace the fresh contents.

2) Don’t invalidate/re-fetch stable config on unrelated refreshes
- If a value is effectively constant for the app’s lifetime (e.g., base URL tied to the current account/backend/environment), resolve it once at startup (or the single appropriate initialization moment) and reuse across later UI refreshes/reconnects.
- Re-fetch only when the value can truly change; otherwise you’ll create unnecessary churn and risk stale/incorrect overwrites.

Example pattern (generation-guarded updates)
```ts
// Pseudocode: per-key generation guarding
const genByKey = new Map<string, number>();

function bumpGen(key: string) {
  genByKey.set(key, (genByKey.get(key) ?? 0) + 1);
}

async function load(key: string) {
  const myGen = genByKey.get(key) ?? 0;
  const result = await fetchForKey(key);

  // Only the latest request is allowed to update state/cache
  if ((genByKey.get(key) ?? 0) !== myGen) return;
  cache.set(key, result);
}

function refreshKey(key: string) {
  bumpGen(key);          // invalidation happens here
  cache.delete(key);
  void load(key);       // starts a new guarded read
}
```

Apply this together with clear invalidation rules: bump generation when you drop/clear cached data, and avoid re-fetching values that are stable across refresh/reconnect.