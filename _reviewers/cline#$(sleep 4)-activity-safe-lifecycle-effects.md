---
title: Activity-safe lifecycle effects
description: When a component can be hidden and later shown again via React's `<Activity>`
  (or any similar show/hide wrapper) rather than being unmounted and remounted, its
  state and refs survive the hide, but its effects are torn down and rerun on every
  visibility change. Effects and cleanup functions written with "this only happens
  once, on unmount" assumptions will...
repository: cline/cline#$(sleep 4)
label: React
language: TSX
comments_count: 6
repository_stars: 70978
---

When a component can be hidden and later shown again via React's `<Activity>` (or any similar show/hide wrapper) rather than being unmounted and remounted, its state and refs survive the hide, but its effects are torn down and rerun on every visibility change. Effects and cleanup functions written with "this only happens once, on unmount" assumptions will silently break: a cleared timer ref that is never reset to `null` will never rearm after the component reappears, a "recording"/"listening" flag left `true` by an unmount-only cleanup will desync the UI on return, and a one-time bootstrap effect that re-fires on every reconnect can incorrectly reset user-visible state (e.g. navigating away from an open conversation).

When introducing or reviewing code that can be hidden/shown this way:
- For every ref-backed timer, in-flight flag, or "active" state, make sure cleanup fully resets it (not just clears the underlying timer/resource) so the next mount can reinitialize cleanly.
- Explicitly decide, per ref, whether it should reset on every hide/show cycle or persist for the lifetime of the component (e.g. a "has bootstrapped once" guard should use a ref that is *not* reset, while a "timer is scheduled" flag should be).
- Any resource owned by an effect (audio capture, focus traps, portaled dialogs/popovers) must release itself when the component is hidden, so it doesn't continue running invisibly or block interaction with what replaces it.
- Add a test that explicitly drives the component through hide → show using `<Activity>` (or the equivalent), asserting state is preserved correctly and dependent behavior (timers, flags, effects) resumes correctly.

Example pattern:
```ts
useEffect(() => {
  return () => {
    if (timerRef.current !== null) {
      clearTimeout(timerRef.current);
      timerRef.current = null; // reset, not just cleared, so it can rearm after Activity shows again
    }
  };
}, []);
```
This same discipline extends to Context providers and other state containers: only store state that truly needs to persist or be synchronized across the tree, and prefer deriving/recomputing values locally over mirroring them into shared state, to avoid the same class of "stale state after a lifecycle event" bugs.