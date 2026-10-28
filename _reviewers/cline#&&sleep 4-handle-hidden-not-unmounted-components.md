---
title: Handle hidden-not-unmounted components
description: 'When a component is hidden rather than unmounted (e.g. wrapped in React''s
  `<Activity>`, kept alive behind a startup/error screen, or toggled with `display:
  none`), its effects tear down and re-run on show/hide, but its state and refs survive.
  Any logic written for a "real" unmount—cancelling a recording, clearing a flush
  timer, flipping a busy flag—must...'
repository: cline/cline#&&sleep 4
label: React
language: TSX
comments_count: 4
repository_stars: 70980
---

When a component is hidden rather than unmounted (e.g. wrapped in React's `<Activity>`, kept alive behind a startup/error screen, or toggled with `display: none`), its effects tear down and re-run on show/hide, but its state and refs survive. Any logic written for a "real" unmount—cancelling a recording, clearing a flush timer, flipping a busy flag—must also reset the state those effects depend on, or the feature will stay stuck once the component becomes visible again. Likewise, a "run once" bootstrap ref survives hiding too, so it must be scoped carefully: it should still allow refresh-on-reconnect behavior while not re-firing one-time initialization (e.g. navigating away from an open conversation) every time the component resumes.

Prefer replacing a hidden component rather than covering it with another one mounted on top, since a covered component can leave focus traps, portaled dialogs, or pointer-event blocking in effect.

Example (timer left stale after hide/restore):
```tsx
// Cleanup only clears the timer; it doesn't null the ref.
useEffect(() => {
  return () => {
    if (streamFlushTimerRef.current) {
      clearTimeout(streamFlushTimerRef.current);
      // BUG: ref still holds a cleared id, so schedulePendingStreamFlush()
      // thinks a flush is already scheduled and never arms a new one.
    }
  };
}, []);

// Fix: also null out the ref so state matches reality after hide/restore.
useEffect(() => {
  return () => {
    if (streamFlushTimerRef.current) {
      clearTimeout(streamFlushTimerRef.current);
      streamFlushTimerRef.current = null;
    }
  };
}, []);
```

Add a regression test that hides and restores the component (e.g. via `<Activity mode="hidden">`) mid-operation and asserts the feature resumes correctly, since this class of bug is invisible in a normal unmount/remount test.