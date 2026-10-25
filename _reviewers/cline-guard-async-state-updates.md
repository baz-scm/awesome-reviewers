---
title: Guard Async State Updates
description: When multiple async operations (fetches, timers, clipboard reads, event
  streams) can overlap, ensure only the newest/authorized result can mutate shared
  state or UI.
repository: CLINE/cline
label: Concurrency
language: TSX
comments_count: 7
repository_stars: 70839
---

When multiple async operations (fetches, timers, clipboard reads, event streams) can overlap, ensure only the newest/authorized result can mutate shared state or UI.

Apply this standard:
1) Add a generation/request id per operation scope (path, fetch type, selection, etc.).
2) After every await (and before any state write), verify the id/generation is still current; otherwise drop the result.
3) For side-effectful handlers that may fire repeatedly (paste/clipboard, repeated clicks), use an in-flight guard so the operation runs once until it settles.
4) For “hide/unmount/mount” scenarios, cleanup must reset concurrency-related refs/timers/flags so the next mount can re-arm correctly.
5) For event-driven state, explicitly track whether events are programmatic vs user-driven (or suspend competing handlers) so one doesn’t incorrectly trigger the other.

Example pattern (generation + guarded write):

```ts
const genRef = useRef(0);
async function load() {
  const gen = ++genRef.current;
  setLoading(true);
  try {
    const result = await fetchSomething();
    if (gen !== genRef.current) return; // stale response
    setData(result);
  } finally {
    if (gen === genRef.current) setLoading(false);
  }
}
function signOut() {
  genRef.current++; // invalidate in-flight work
  setLoading(false);
}
```

Checklist to use in code review:
- “What happens if this request resolves after a newer selection/navigation/sign-out?”
- “Can this handler run twice before the async work settles?”
- “Does cleanup/reset allow correct behavior after hide/show or remount?”
- “Are we misclassifying programmatic events as user intent (or failing to suspend competing listeners)?”