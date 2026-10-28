---
title: Effect cleanup for remounts
description: When a component can be unmounted and remounted while preserving its
  internal state (e.g. toggled with React's `<Activity>`, or kept alive behind a conditional
  render instead of being torn down), every effect's cleanup must leave refs and flags
  in a state that lets the effect behave correctly next time it runs — not in a "permanently
  done" state that only...
repository: cline/cline#`sleep 4`
label: React
language: TSX
comments_count: 7
repository_stars: 70979
---

When a component can be unmounted and remounted while preserving its internal state (e.g. toggled with React's `<Activity>`, or kept alive behind a conditional render instead of being torn down), every effect's cleanup must leave refs and flags in a state that lets the effect behave correctly next time it runs — not in a "permanently done" state that only made sense for a true unmount.

Concretely:
- If an effect's cleanup clears a timer/interval, it must also null out the ref that tracks it, so the next mount re-arms a fresh timer instead of silently doing nothing (e.g. a stream-flush timer cleared on hide but never reset left buffered text stuck after the component reappeared).
- If an effect's cleanup cancels an in-progress operation (recording, a controller), it must also reset any state booleans (`isListening`, `isProcessing`) that same tick, so the UI doesn't resume believing an operation is still active.
- One-time bootstrap effects (initial navigation, initial selection) that must run only once across remounts should use a ref flag set after success, not `useState`/plain variables that get reinitialized — but refreshable side effects (e.g. re-fetching environment status) should still run every mount.
- Expensive or must-run-once-globally async setup shared across remounts should be memoized outside the component (module scope) so repeated mounts reuse the settled promise instead of re-triggering the work.
- Prefer replacing a mounted subtree with a hidden/inert one (or `<Activity mode="hidden">`) over covering it with an overlay, so background dialogs/popovers actually release focus traps and `pointer-events` instead of staying mounted underneath.

Example of the pattern to apply to every effect touching a ref-backed timer or flag:

```tsx
useEffect(() => {
  return () => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null; // not just cleared — reset so re-mount re-arms it
    }
    isRecordingRef.current = false; // reset flags too, not just cancel the operation
  };
}, []);
```

Treat every "unmount" cleanup as something that may run while the component's state is otherwise being kept alive, and verify with a test that hides/shows (or unmounts/remounts) the component mid-operation.