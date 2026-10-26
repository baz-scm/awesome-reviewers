---
title: Sync Async State Updates
description: When async work can overlap (multiple refreshes, in-flight fetches, repeated
  user actions, polling, or remount/hide/show causing effect re-runs), you must explicitly
  synchronize side effects so stale results can’t overwrite newer state and duplicate
  actions can’t run.
repository: cline/cline#v13
label: Concurrency
language: TSX
comments_count: 8
repository_stars: 70874
---

When async work can overlap (multiple refreshes, in-flight fetches, repeated user actions, polling, or remount/hide/show causing effect re-runs), you must explicitly synchronize side effects so stale results can’t overwrite newer state and duplicate actions can’t run.

Apply these rules:
1) Use generation/version tokens for async results that can arrive out of order.
- Increment a ref before starting the request.
- After each await, check the ref (or token) before writing state.
- Also bump the token on “invalidate” events (sign out, mode switches, cancel/close).

```ts
const genRef = useRef(0);
const refresh = useCallback(async () => {
  const gen = ++genRef.current;
  setRefreshing(true);
  try {
    const next = await api.getStatus();
    if (gen !== genRef.current) return; // stale
    setStatus(next);
  } finally {
    if (gen === genRef.current) setRefreshing(false);
  }
}, []);

const signOut = useCallback(() => {
  genRef.current++; // invalidate in-flight writes
  doSignOut();
}, []);
```

2) Use single-flight (in-flight guards) for user-triggered side effects that must not duplicate.
- Example: guard clipboard reads, sandbox create calls, or “open details” actions so the second trigger either waits or no-ops until the first finishes.

3) Make “run once” semantics robust to remount/effect re-execution.
- Use stable refs to gate one-time bootstrap actions after the first successful initialization.
- Still allow refresh-on-reconnect separately.

4) Ensure cleanup resets scheduler/timer state and intent tracking.
- Clear pending timeouts/intervals and null out refs in effect cleanup.
- If behavior must resume after re-show, re-arm scheduling from the next mount/visible transition.

5) Separate programmatic vs user intent when interpreting events.
- Track intent targets (e.g., scroll-to-bottom initiated by code) so resulting events don’t trigger the wrong state transition.

Outcome: state updates become deterministic, stale responses are safely ignored, duplicate side effects are prevented, and hide/show or rapid repeated inputs no longer corrupt UI state.