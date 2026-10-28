---
title: Activity-aware effect lifecycle
description: When preserving a subtree's state across visibility changes (e.g. React's
  `<Activity>`, or any hide/show pattern that keeps a component mounted instead of
  unmounting it), remember that effects still run their cleanup on hide and re-run
  their setup on show — only component state and refs persist. Auditing every effect
  against this is required before relying...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TSX
comments_count: 6
repository_stars: 70965
---

When preserving a subtree's state across visibility changes (e.g. React's `<Activity>`, or any hide/show pattern that keeps a component mounted instead of unmounting it), remember that effects still run their cleanup on hide and re-run their setup on show — only component state and refs persist. Auditing every effect against this is required before relying on such a pattern:

1. **Prefer hide-in-place over remount or overlay**. Unmounting on a transient failure loses state and reruns expensive setup; covering the app with an overlay instead of replacing it can leave a portaled dialog's focus trap or `pointer-events: none` active underneath. Replace the visible tree with the fallback (or hide it via `Activity`) rather than stacking content on top of it.

2. **Cleanup must fully reset transient state, not just cancel it**. A cleanup that clears a timer/interval but leaves its ref pointing at the stale ID will prevent any future scheduling call from ever arming a new one, since that call sees a "timer already pending" ref. Always null out the ref alongside cancelling:
```ts
useEffect(() => {
  return () => {
    if (timerRef.current != null) {
      clearTimeout(timerRef.current);
      timerRef.current = null; // required so a later effect run can re-arm it
    }
  };
}, []);
```
   The same applies to externally-owned side effects (e.g. a recording/listening session kept outside React state): cancelling the operation on cleanup must also reset the flags that drive the UI, so the component doesn't resume believing a cancelled operation is still in progress.

3. **Guard "run once" effects with a ref, not mount semantics**. An effect meant to bootstrap state only on the component's first real initialization (e.g., an initial navigation dispatch) will re-fire every time a hidden subtree becomes visible again, since refs survive hiding but effects do not persist across the hide/show boundary. Use a ref flag to distinguish the true first run from a later resume:
```ts
const bootstrapped = useRef(false);
useEffect(() => {
  refreshSomething(); // safe to rerun every time
  if (!bootstrapped.current) {
    bootstrapped.current = true;
    dispatchInitialNavigation(); // only once, ever
  }
}, [dependency]);
```

Add a test that hides and re-shows the component (or exercises the fallback/overlay path) mid-operation and asserts both the resumed UI state and any pending async work (timers, streams, bootstrap dispatches) behave correctly — this class of bug is invisible without explicitly simulating the hide/show cycle.