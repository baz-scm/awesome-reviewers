---
title: Guard async state updates
description: When async work can finish out of order (fetches), re-enter (rapid events),
  or outlive UI assumptions (hide/unmount), you must prevent stale or duplicate side
  effects.
repository: cline/cline#v1
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70862
---

When async work can finish out of order (fetches), re-enter (rapid events), or outlive UI assumptions (hide/unmount), you must prevent stale or duplicate side effects.

Practical rules:
1) Version/generation-check before committing state
- When starting an async load, increment a per-key generation (or capture a token). After every await, confirm the token/gen is still current; otherwise do nothing.

2) Avoid captured stale state in async callbacks
- If an async callback persists/updates derived data, ensure it reads the latest selection/state (e.g., via a ref updated on render, or a functional updater that receives current state).

3) Use in-flight guards for re-entrant handlers
- For user actions that can trigger repeated async reads (clipboard, double clicks), keep a “pending” ref and return early while it’s set.

4) Clean up timers/locks on hide/unmount
- When UI visibility changes or components unmount, clear timers and null any refs used by schedulers so they re-arm correctly on restore.

Example pattern (generation + latest-state + cleanup):
```ts
const genRef = useRef(new Map<string, number>());
const inFlightRef = useRef(false);

const load = useCallback(async (key: string, query: string) => {
  const genMap = genRef.current;
  const nextGen = (genMap.get(key) ?? 0) + 1;
  genMap.set(key, nextGen);

  // Optional: in-flight guard for a specific action type
  if (inFlightRef.current) return;
  inFlightRef.current = true;

  try {
    const result = await fetchSomething(query);

    // Drop stale responses
    if ((genRef.current.get(key) ?? 0) !== nextGen) return;

    // Commit only if still current
    setState((prev) => apply(result, prev));
  } finally {
    // Release in-flight
    setTimeout(() => { inFlightRef.current = false; }, 100);
  }
}, []);

useEffect(() => {
  return () => {
    // Cleanup timers/refs so restore doesn’t stall
    clearTimeout(timerRef.current ?? undefined);
    timerRef.current = null;
  };
}, []);
```

Adopt this standard for:
- async fetches that update UI state
- persistence updates that depend on user selection
- clipboard/paste handlers
- visibility/hide/unmount scenarios with pending timers/flushes