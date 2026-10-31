---
title: Activity-aware effect cleanup
description: 'When using React''s `<Activity>` (or any keep-alive hide/show pattern)
  to preserve a subtree''s state instead of unmounting it, remember that hiding tears
  down effects just like an unmount would, but mounting back only reruns them — it
  does not reset state that effects set outside of cleanup. Two failure modes recur:'
repository: cline/cline?foo=bar
label: React
language: TSX
comments_count: 5
repository_stars: 71082
---

When using React's `<Activity>` (or any keep-alive hide/show pattern) to preserve a subtree's state instead of unmounting it, remember that hiding tears down effects just like an unmount would, but mounting back only reruns them — it does not reset state that effects set outside of cleanup. Two failure modes recur:

1. **Stale flags/timers after hide.** An effect's cleanup written only for "this is going away forever" (e.g. clearing a timer ref, cancelling a recording) must also reset any state/flags that effect owns, or that state survives the hide and is wrong once the subtree becomes visible again. Pattern: on cleanup, null out the ref/flag the effect's scheduler checks before re-arming, not just the timer handle itself.

```ts
useEffect(() => {
  return () => {
    if (timerRef.current) clearTimeout(timerRef.current);
    timerRef.current = null; // without this, the next "resume" never re-arms
  };
}, []);
```

2. **One-time bootstrap effects re-firing on resume.** An effect that should run its side effect (e.g. initial navigation, selecting a default) only once on first successful load will rerun every time Activity remounts it (e.g. after a reconnect), clobbering user state such as the active conversation. Guard the one-shot behavior with a `ref` — refs survive Activity's hide/show cycle — so later reruns can still refresh derived data but skip the one-time action.

```ts
const bootstrapped = useRef(false);
useEffect(() => {
  loadContext().then((ctx) => {
    refreshDerivedState(ctx);           // safe to repeat
    if (!bootstrapped.current) {
      bootstrapped.current = true;
      dispatchInitialNavigation(ctx);   // only once, ever
    }
  });
}, [dep]);
```

Prefer `<Activity mode="hidden">` over unmounting when you need to preserve expensive state (open conversations, scroll position) while still releasing focus traps, body `pointer-events`, and other effect-driven side effects of portaled dialogs/popovers underneath. But audit every effect in the hidden subtree for implicit "only fires on true unmount" assumptions, and add regression tests that hide and re-show the component mid-operation (mid-stream, mid-recording, mid-bootstrap) to catch state that silently survives in the wrong shape.