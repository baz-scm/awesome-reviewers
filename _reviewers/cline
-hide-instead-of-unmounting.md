---
title: Hide instead of unmounting
description: When a component's state must survive being toggled off-screen (e.g.
  an app view behind a startup/error screen, a tab switch, a temporarily-disabled
  panel), don't conditionally mount/unmount it. Unmounting discards state (open conversation,
  draft text, in-flight timers) and can leave stale dialogs/popovers mounted behind
  an overlay, trapping focus or...
repository: 'cline/cline

  '
label: React
language: TSX
comments_count: 5
repository_stars: 70942
---

When a component's state must survive being toggled off-screen (e.g. an app view behind a startup/error screen, a tab switch, a temporarily-disabled panel), don't conditionally mount/unmount it. Unmounting discards state (open conversation, draft text, in-flight timers) and can leave stale dialogs/popovers mounted behind an overlay, trapping focus or blocking `pointer-events` on the body. Instead, keep the component mounted and toggle its visibility with a mount-preserving mechanism such as React's `<Activity mode="visible" | "hidden">`. This keeps component state intact while still running effect cleanup on hide, so portaled dialogs release their focus traps and the DOM is actually hidden.

Because cleanup still runs on hide (even though the component isn't destroyed), treat every effect's cleanup as "this effect is stopping, not just unmounting forever": explicitly reset any state a live effect assumed it owned, not only cancel its timer or async work. A cleanup that clears `setInterval` but leaves the ref pointing at the old (now invalid) timer ID will make the scheduler think a timer is already running when the component is shown again, so a re-arm never happens and buffered work (e.g. streamed text) is silently lost. Likewise, a cleanup that cancels a recording but leaves `isListening`/`isProcessing` `true` leaves the UI showing an active state that no longer reflects reality once the component reappears. The fix in both cases is the same: cleanup must null out/reset every flag or ref the effect set, in addition to stopping the underlying work, so the component reinitializes cleanly the next time it becomes visible.

```tsx
useEffect(() => {
  schedulePendingFlush(); // may arm streamFlushTimerRef.current
  return () => {
    clearTimeout(streamFlushTimerRef.current);
    streamFlushTimerRef.current = null; // not just clearTimeout — reset the flag too
  };
}, []);
```

Prefer this hide/show pattern over remount-based conditional rendering whenever the hidden state needs to come back exactly as it was, and audit every effect's cleanup to make sure it fully un-does the effect's side effects, not just the parts that would matter on a real unmount.