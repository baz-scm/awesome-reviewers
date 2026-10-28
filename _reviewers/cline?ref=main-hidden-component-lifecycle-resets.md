---
title: Hidden-component lifecycle resets
description: When a component can be hidden-without-unmounting (React's `<Activity>`,
  manual conditional show/hide, portal-based overlays kept mounted, etc.), its state,
  refs, and timers survive the toggle — unlike a real unmount/remount. Effects written
  with only "real unmount" in mind will leave stale flags or dangling refs that break
  the component the next time it...
repository: cline/cline?ref=main
label: React
language: TSX
comments_count: 4
repository_stars: 70980
---

When a component can be hidden-without-unmounting (React's `<Activity>`, manual conditional show/hide, portal-based overlays kept mounted, etc.), its state, refs, and timers survive the toggle — unlike a real unmount/remount. Effects written with only "real unmount" in mind will leave stale flags or dangling refs that break the component the next time it becomes visible.

Apply two rules to any effect in a component that may be hidden this way:

1. **Cleanup must fully reset state, not just cancel work.** If an effect's cleanup clears a timer, cancels a recording, or aborts a request, it must also reset any state/ref that reflects "this is in progress" (e.g. `streamFlushTimerRef.current = null`, `isListening`/`isProcessing` flags) back to the idle value. Otherwise the scheduler that relies on "ref is null → arm a new timer" never fires again, or a callback like `onActiveChange(false)` never gets called once the component resurfaces.

2. **One-time bootstrap effects need a guard that survives re-activation.** An effect meant to run its side effect ("select a default", "navigate to initial route") only once on first successful load will re-fire every time the component is hidden and shown again, because the effect itself remounts. Track "has this succeeded before" in a ref (refs persist across hide/show) and gate the one-time side effect on it, while still letting the rest of the effect's logic (e.g. refreshing data) run on every activation.

Example:
```tsx
function useRemoteEnvironmentBootstrap() {
  const bootstrappedRef = useRef(false);

  useEffect(() => {
    let cancelled = false;
    getProcessContext().then((context) => {
      if (cancelled) return;
      refreshActiveEnvironment(context); // always refresh
      if (!bootstrappedRef.current) {
        bootstrappedRef.current = true;
        dispatch(selectEnvironmentDraft(context)); // only once, ever
      }
    });
    return () => { cancelled = true; };
  }, []);
}

function useStreamFlush() {
  const timerRef = useRef<number | null>(null);
  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
      timerRef.current = null; // restore idle state, not just stop the timer
    };
  }, []);
}
```

Add regression tests that hide and re-show the component (e.g. via `<Activity mode="hidden">` then `"visible"`) and assert behavior resumes correctly — this class of bug is invisible in tests that only mount once.