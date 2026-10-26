---
title: Stale Async Guarding
description: 'When async operations can overlap (user switching, refresh, polling,
  visibility toggles), never let stale or duplicated results write to state/storage.
  Use one of these patterns:'
repository: cline/cline#v23
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70889
---

When async operations can overlap (user switching, refresh, polling, visibility toggles), never let stale or duplicated results write to state/storage. Use one of these patterns:

1) Generation (or per-key) tokens for “latest-wins”
- Assign a monotonically increasing generation per request scope (global for the operation, or per-key like a path).
- Capture it when starting the async work.
- After every await (or before any state write), check that the captured generation still matches the latest.
- Invalidation events (sign-out, new refresh, new navigation, new request) must bump the generation.

2) In-flight guards for duplicate side effects
- For async side effects triggered multiple times (clipboard reads, rapid clicks), add an in-flight ref/lock.
- If a read is already pending, return early.

3) Cleanup must reset schedulers/flags
- When components are hidden/unmounted/remounted (e.g., Activity visibility), cleanup should reset timer refs and relevant state flags so re-showing re-arms scheduling and doesn’t leave stale “enabled/inactive/loading” states.

Example (generation pattern):
```ts
const genRef = useRef(0);

async function load(resourceId: string) {
  const myGen = ++genRef.current;
  setLoading(true);

  const result = await fetchSomething(resourceId);

  // Drop stale results
  if (myGen !== genRef.current) return;

  // Safe state writes only for the latest request
  setData(result);
  setLoading(false);
}

function invalidate() {
  genRef.current++; // bumps to invalidate in-flight work
  setLoading(false);
}
```

Apply this standard to: overlapping fetches (with/without polling), async reads after user actions, and any background timer/stream flush whose scheduling depends on component visibility.