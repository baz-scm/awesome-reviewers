---
title: Reset state on Activity resume
description: When a subtree is hidden/shown with React's `<Activity>` (or any similar
  show/hide pattern) instead of being unmounted and remounted, effects tear down and
  re-run their setup each time visibility toggles, but their cleanup functions still
  only run the "true unmount" logic. Any mutable ref, timer id, or boolean flag that
  the cleanup assumed would be thrown...
repository: "cline/cline\t"
label: React
language: TSX
comments_count: 5
repository_stars: 70947
---

When a subtree is hidden/shown with React's `<Activity>` (or any similar show/hide pattern) instead of being unmounted and remounted, effects tear down and re-run their setup each time visibility toggles, but their cleanup functions still only run the "true unmount" logic. Any mutable ref, timer id, or boolean flag that the cleanup assumed would be thrown away with the component silently survives and goes stale, so re-running the setup on resume can skip rearming a timer, leave a "recording"/"listening" flag stuck true, or let a one-shot bootstrap effect fire again and clobber state a user already changed.

When writing an effect that may be hidden and shown again rather than unmounted:
- In the cleanup, explicitly reset every ref/flag the setup function checks before deciding what to do (e.g. set a timer ref back to `null` after clearing it, not just clear the timeout), so the next run's setup behaves as if it is starting fresh.
- For logic that must run only once ever (e.g. an initial navigation/bootstrap dispatch), gate it with a ref flag that is only set after the action truly succeeds, not merely "effect ran once" — refs survive hide/show, so this correctly suppresses a repeat without needing to detect whether the remount was real.
- Prefer deriving UI-critical reads (like "is this feed still current") from the source of truth on each run rather than caching a value that an interrupted or restarted effect could leave stale.
- Add a test that hides and re-shows the component mid-operation (e.g. mid-recording, mid-stream, mid-async-load) and asserts the resumed state matches what a continuous mount would produce.

Example:
```tsx
useEffect(() => {
  return () => {
    clearTimeout(timerRef.current);
    timerRef.current = null; // not just cleared — reset so the next setup rearms it
  };
}, []);
```