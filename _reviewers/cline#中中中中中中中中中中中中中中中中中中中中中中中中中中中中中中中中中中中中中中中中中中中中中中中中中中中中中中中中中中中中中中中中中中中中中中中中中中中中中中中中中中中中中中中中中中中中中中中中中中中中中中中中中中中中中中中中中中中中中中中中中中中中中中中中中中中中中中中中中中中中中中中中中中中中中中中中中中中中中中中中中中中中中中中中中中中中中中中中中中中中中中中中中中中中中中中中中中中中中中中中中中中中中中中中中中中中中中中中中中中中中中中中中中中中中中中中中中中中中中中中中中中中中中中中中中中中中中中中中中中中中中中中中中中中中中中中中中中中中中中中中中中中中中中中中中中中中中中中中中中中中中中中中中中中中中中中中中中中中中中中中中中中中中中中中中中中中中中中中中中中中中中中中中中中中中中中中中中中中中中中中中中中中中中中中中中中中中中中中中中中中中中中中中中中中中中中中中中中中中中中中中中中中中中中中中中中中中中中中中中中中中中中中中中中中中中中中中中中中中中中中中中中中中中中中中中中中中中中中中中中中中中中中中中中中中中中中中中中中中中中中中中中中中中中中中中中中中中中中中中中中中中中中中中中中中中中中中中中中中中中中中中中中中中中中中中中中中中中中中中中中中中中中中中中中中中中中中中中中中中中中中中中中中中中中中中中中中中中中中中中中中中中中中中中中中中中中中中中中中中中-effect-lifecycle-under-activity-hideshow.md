---
title: Effect lifecycle under Activity hide/show
description: When a subtree can be hidden and shown again (e.g. wrapped in React's
  `<Activity>`, or any "cover instead of unmount" pattern) rather than unmounted and
  remounted, its effects are torn down on hide and rerun on show while component state
  and refs survive. Any effect written with an "unmount-only" mental model will misbehave
  the first time it runs on a...
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: React
language: TSX
comments_count: 6
repository_stars: 70984
---

When a subtree can be hidden and shown again (e.g. wrapped in React's `<Activity>`, or any "cover instead of unmount" pattern) rather than unmounted and remounted, its effects are torn down on hide and rerun on show while component state and refs survive. Any effect written with an "unmount-only" mental model will misbehave the first time it runs on a hide/show cycle instead of a true unmount, so audit effects for these failure modes:

1. **Cleanup must reset in-progress state, not just cancel it.** If a cleanup function cancels a timer, recording session, or stream flush but leaves a ref/flag (e.g. `streamFlushTimerRef.current`, `isListening`) pointing at the old (now-dead) resource, the effect's re-run on show will see "already active" and never re-arm, silently dropping buffered work. Null out or reset every piece of state the cleanup invalidates.

2. **Distinguish "run once ever" from "run once per mount" with refs that outlive hiding.** A bootstrap effect that dispatches a one-time navigation/initialization action will fire again on every show if it isn't guarded. Use a ref flag set only on the first *successful* run (failed/cancelled attempts shouldn't count), and keep data-refreshing logic (e.g. refetching remote status) separate from the one-time side effect so reconnects still refresh data without repeating the one-time action.

3. **Portaled/overlay elements (dialogs, popovers) must release focus traps and global side effects on hide exactly as they would on unmount.** Verify there's no state where a dialog is still mounted-but-hidden with `pointer-events` or a focus trap still applied, which would make the underlying UI unreachable.

4. **Memoize expensive one-time setup at module scope when it must survive remounts/retries**, rather than re-invoking it from an effect that reruns on every show, especially for operations with side effects that shouldn't repeat (e.g. "kill all previous sessions" on startup).

Add a regression test that explicitly hides and re-shows the component (or simulates the equivalent teardown/rerun) and asserts state recovers correctly, since this class of bug is invisible in a standard mount/unmount test.

Example pattern for safe cleanup:
```tsx
useEffect(() => {
  const timer = schedulePendingFlush();
  streamFlushTimerRef.current = timer;
  return () => {
    clearTimeout(timer);
    // Without this, a later show() sees a stale non-null ref and
    // skips re-arming the flush, so buffered text is lost.
    streamFlushTimerRef.current = null;
  };
}, [...]);

// Bootstrap-once guard that survives Activity hiding (refs persist):
const bootstrappedRef = useRef(false);
useEffect(() => {
  loadContext().then((result) => {
    refreshEnvironment(result); // always refresh
    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      dispatch({ type: "select-environment-draft", result }); // once only
    }
  });
}, [...]);
```