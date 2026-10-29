---
title: Effect cleanup for Activity
description: When a subtree can be hidden and shown again without a true unmount (React's
  `Activity`, or any "keep state, pause effects" pattern), effect cleanup functions
  must fully reset state, not just cancel in-flight work. `Activity` runs effect cleanup
  on hide and reruns the effect on show, but refs and state survive the hide — so
  a cleanup written for "this only...
repository: cline/cline#1
label: React
language: TSX
comments_count: 6
repository_stars: 71024
---

When a subtree can be hidden and shown again without a true unmount (React's `Activity`, or any "keep state, pause effects" pattern), effect cleanup functions must fully reset state, not just cancel in-flight work. `Activity` runs effect cleanup on hide and reruns the effect on show, but refs and state survive the hide — so a cleanup written for "this only happens once, at real unmount" silently breaks the component the second time it's shown.

Concretely: if an effect clears a timer/flag on cleanup but never nulls the ref that guards re-arming it, the timer never gets scheduled again after the component is shown, and pending work (e.g. buffered streamed text) is lost. Similarly, a boolean flag like `isListening` cleared only via a cancel callback can get stuck true if the cancel didn't fire before hide, leaving downstream consumers out of sync after resume. One-time bootstrap effects (e.g. "pick the initial selection") need a ref that distinguishes "ran once successfully" from "is currently running," so a hide/show cycle mid-flight doesn't either skip a needed re-fetch or incorrectly repeat a one-time side effect (like navigating away from a conversation the user already opened).

Standard:
- Treat cleanup as "prepare to run again," not "final teardown." Reset every ref/flag the effect depends on, not just the one directly tied to the cancelled operation.
- For one-shot bootstrap logic, guard with a ref that only flips after a *successful* first run, and make clear which parts of the effect should still rerun on every show (e.g. refreshing data) versus only once (e.g. initial navigation).
- Add a test that hides and shows the component mid-operation (via `<Activity mode="hidden"/visible">`) and asserts the pending behavior resumes correctly, not just that mount/unmount works.

```ts
// Bad: timer ref is cleared but never reset, so a flush scheduled
// before hide can never be rescheduled after show.
useEffect(() => {
  return () => {
    if (streamFlushTimerRef.current) {
      clearTimeout(streamFlushTimerRef.current);
    }
  };
}, []);

// Good: cleanup leaves the ref ready for the next effect run.
useEffect(() => {
  return () => {
    if (streamFlushTimerRef.current) {
      clearTimeout(streamFlushTimerRef.current);
      streamFlushTimerRef.current = null;
    }
  };
}, []);
```