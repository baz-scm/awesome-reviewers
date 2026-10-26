---
title: Guard Against Async Races
description: When async work (fetches, clipboard reads, timers) and event handlers
  can overlap, always prevent stale or duplicated side effects. Use a monotonic “latest”
  token and explicit locks/suspensions.
repository: cline/cline#v10
label: Concurrency
language: TSX
comments_count: 6
repository_stars: 70869
---

When async work (fetches, clipboard reads, timers) and event handlers can overlap, always prevent stale or duplicated side effects. Use a monotonic “latest” token and explicit locks/suspensions.

**Coding standards**
1. **Stale response protection (generation/requestId):**
   - Before `await`, capture a token (e.g., `requestId`/`generation`).
   - After `await` and before any `setState`/state writes, verify the token is still current; otherwise drop the result.
   - Bump the token on “cancel” events (e.g., Sign Out, switching views, new request).

2. **Duplicate side-effect prevention (in-flight guard):**
   - For event paths that trigger async reads whose result must be applied exactly once (clipboard/system clipboard), guard with a single in-flight ref/lock.
   - If already in-flight, return early.
   - Release the lock after the operation settles (or with a short debounce window).

3. **Mode-based suspension:**
   - During critical UI modes (e.g., shortcut recording), suspend other related handlers using a shared “suspended” flag, and ensure all listeners consult it.

4. **Lifecycle/timer cleanup:**
   - On hide/unmount, clear timers/intervals and reset timer refs (e.g., set ref to `null`) so re-mount reliably re-arms scheduling.

**Example pattern (token + latest check)**
```ts
const genRef = useRef(0);

useEffect(() => {
  const myGen = ++genRef.current;
  (async () => {
    const result = await fetchSomething();
    if (genRef.current !== myGen) return; // stale -> drop
    setData(result);
  })();
}, [/* deps that trigger new request */]);

function cancel() {
  genRef.current++; // invalidates in-flight responses
}
```

Applying these rules will prevent: stale async overwrites, state updates after cancellation, duplicate event outcomes, and timer/toggle races.