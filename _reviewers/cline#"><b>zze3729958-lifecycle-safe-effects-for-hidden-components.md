---
title: Lifecycle-safe effects for hidden components
description: When a component can be hidden and later shown again (e.g. wrapped in
  `<Activity>`, or kept mounted behind a cover screen instead of unmounted) rather
  than destroyed, its effects must be written to survive that cycle correctly, not
  just a terminal unmount.
repository: cline/cline#"><b>zze3729958
label: React
language: TSX
comments_count: 6
repository_stars: 71067
---

When a component can be hidden and later shown again (e.g. wrapped in `<Activity>`, or kept mounted behind a cover screen instead of unmounted) rather than destroyed, its effects must be written to survive that cycle correctly, not just a terminal unmount.

Key rules:
- Prefer hiding over conditional unmounting for stateful subtrees (open conversations, dialogs). Unmounting loses state and can leave a cover screen stacked on top of still-mounted dialogs/portals, trapping focus or blocking pointer events. Hiding (e.g. React `Activity`) tears down effects and detaches the DOM so focus traps and `pointer-events` locks release correctly, while state (refs, component state) is preserved.
- Any cleanup function written assuming "this only runs once, on real unmount" must also handle being called when the component is merely hidden. If a cleanup clears a timer/flag but doesn't reset the ref that gates re-arming it, the effect will never restart when the component is shown again:

```ts
// Before: breaks after hide/show — timer ref stays non-null
useEffect(() => {
  return () => {
    if (timerRef.current) clearTimeout(timerRef.current);
  };
}, []);

// After: resets the gate so the next schedule call re-arms a timer
useEffect(() => {
  return () => {
    if (timerRef.current) {
      clearTimeout(timerRef.current);
      timerRef.current = null;
    }
  };
}, []);
```
  The same applies to boolean state flags (e.g. `isListening`/`isProcessing`) that a consumer reads to decide UI state — reset them in cleanup so the consumer isn't left out of sync when the component reappears.
- One-time bootstrap/initialization effects (e.g. navigating to a default route on first successful load) must track "has this run" with a ref that survives hide/show, not rely on "this is the first render" — Activity/resume re-runs effects, so a naive re-run can re-trigger navigation or reset state the user already changed. Gate the one-time side effect behind a ref while still allowing idempotent parts of the effect (e.g. refreshing data) to run on every resume.
- Add regression tests that explicitly hide and re-show the component (or simulate the resume) and assert state/behavior that depends on effect re-initialization still works.