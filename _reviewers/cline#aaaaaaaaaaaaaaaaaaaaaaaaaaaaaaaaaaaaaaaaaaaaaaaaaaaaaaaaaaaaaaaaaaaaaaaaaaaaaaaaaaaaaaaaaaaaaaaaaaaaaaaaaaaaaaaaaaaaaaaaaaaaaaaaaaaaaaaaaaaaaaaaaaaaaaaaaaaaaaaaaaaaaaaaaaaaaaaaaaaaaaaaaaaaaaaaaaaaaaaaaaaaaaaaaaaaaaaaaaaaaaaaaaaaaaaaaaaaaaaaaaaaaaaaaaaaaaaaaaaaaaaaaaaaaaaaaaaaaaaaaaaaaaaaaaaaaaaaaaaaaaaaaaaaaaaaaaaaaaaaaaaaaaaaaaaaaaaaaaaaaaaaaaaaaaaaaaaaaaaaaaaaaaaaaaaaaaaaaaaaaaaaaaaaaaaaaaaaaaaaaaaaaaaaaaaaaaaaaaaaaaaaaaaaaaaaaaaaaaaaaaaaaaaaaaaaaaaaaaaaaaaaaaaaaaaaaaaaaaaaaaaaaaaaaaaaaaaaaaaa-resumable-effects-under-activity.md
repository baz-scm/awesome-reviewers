---
title: Resumable effects under Activity
description: When a subtree is hidden instead of unmounted (React's `<Activity mode="hidden">`,
  or an equivalent "cover but keep mounted" pattern), its component state and refs
  survive, but effects are torn down and re-run on resume. Any cleanup logic written
  for a true unmount — clearing a timer, cancelling a recording, resetting a "has
  bootstrapped" flag — must also...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TSX
comments_count: 5
repository_stars: 70964
---

When a subtree is hidden instead of unmounted (React's `<Activity mode="hidden">`, or an equivalent "cover but keep mounted" pattern), its component state and refs survive, but effects are torn down and re-run on resume. Any cleanup logic written for a true unmount — clearing a timer, cancelling a recording, resetting a "has bootstrapped" flag — must also reset the mutable refs/state that effect depends on, or the resumed effect will see stale data and silently stop working (e.g. a stream-flush timer whose ref still points to a cleared id never reschedules; a recording flag stuck "true" after the mic was stopped).

Concretely:
- In cleanup functions, null out/reset any ref the effect uses to decide whether to (re)initialize, not just the side effect itself:
```ts
useEffect(() => {
  streamFlushTimerRef.current = setTimeout(flush, interval);
  return () => {
    clearTimeout(streamFlushTimerRef.current);
    streamFlushTimerRef.current = null; // without this, resume never reschedules
  };
}, []);
```
- For one-time bootstrap effects (initial navigation, initial data load) that must not re-fire every time the subtree becomes visible again, guard them with a ref (refs survive hiding) rather than relying on the effect only running once — split "run once ever" logic from "refresh on every become-visible" logic into separate effects/hooks.
- Prefer replacing a failed or not-yet-ready view with its fallback (`ready ? <App/> : <Fallback/>`) rather than stacking the fallback on top of a still-mounted app; a hidden-but-mounted app can keep a focus trap or portal open underneath, and two sets of window controls/dialogs can end up mounted at once.
- Add a regression test that hides and re-shows the component (or toggles the gating condition) mid-operation and asserts the behavior resumes correctly, since these bugs are invisible in a normal mount/unmount test.