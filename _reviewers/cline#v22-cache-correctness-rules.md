---
title: Cache correctness rules
description: 'When caching influences user-visible behavior or recovery logic, treat
  caches as lifecycle-scoped snapshots, not just “memoized values”.


  Apply these rules:'
repository: cline/cline#v22
label: Caching
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When caching influences user-visible behavior or recovery logic, treat caches as lifecycle-scoped snapshots, not just “memoized values”.

Apply these rules:
1) Cache identity must include all relevant inputs/state.
- If behavior depends on mode, enabled/disabled flags, or workspace/account scope, the cache key must change when those change.

2) Diffs/recovery baselines must be captured at cache-build time.
- If you compute “what changed” after reconnect/recovery, compare against the snapshot that matches the tools/data the session actually uses, not whatever the latest refresh wrote.

3) Invalidate dependent caches before reposting derived state.
- When a setting toggles which rows are included (e.g., cloud sessions in history), invalidate the downstream cache first so the next state post re-enumerates consistently.

4) TTL-driven refresh should be behind-the-scenes to avoid flicker.
- Serve cached data until TTL expiry, then reload in the background; keep the UI stable while the fetch updates caches.

5) Failure caching needs backoff + retry when change detection can’t see fixes.
- If a failure might be transient or a fix could be invisible to fingerprint/change detection, store failure with a retry delay and retry later (but avoid infinite retry loops).

Sketch (baseline + TTL + invalidation + backoff pattern):
```ts
// 1) Snapshot baseline tied to when tools were built
const baseline = this.surfaceBuiltFromToolsSessionId;

// 2) Serve cached while TTL not expired; refresh behind scenes
if (now - lastFetchedAt < TTL) return cached;
void refresh().catch(() => {
  // 3) Failure backoff so we retry later
  lastFailureAt = now;
});

// 4) On setting change, invalidate dependent cache before posting state
function onCloudSessionsEnabledChanged(enabled: boolean) {
  taskHistoryCache.invalidate();
  postStateToWebview();
}
```