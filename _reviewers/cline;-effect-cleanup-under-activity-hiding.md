---
title: Effect cleanup under Activity hiding
description: When a component can be hidden (e.g. wrapped in React's `<Activity>`)
  rather than unmounted, its effects still run their cleanup on hide and re-run their
  setup on show, but any ref-held state (timers, in-flight flags, "has this run once"
  markers) survives since refs are not reset by React. Cleanup functions written only
  for true unmount therefore leave this...
repository: cline/cline;
label: React
language: TSX
comments_count: 4
repository_stars: 70964
---

When a component can be hidden (e.g. wrapped in React's `<Activity>`) rather than unmounted, its effects still run their cleanup on hide and re-run their setup on show, but any ref-held state (timers, in-flight flags, "has this run once" markers) survives since refs are not reset by React. Cleanup functions written only for true unmount therefore leave this transient state wrong: a cleared timer ref left non-null blocks the next scheduler from re-arming, a cancelled "recording"/"listening" flag that isn't reset never reaches the UI once shown again, and a one-shot bootstrap effect with no "already ran" ref re-fires every time the component is shown, re-triggering navigation or other side effects it was only meant to do once.

When writing an effect whose cleanup may run from a hide (not just a true unmount):
- Reset every ref-held flag or handle the cleanup touches, not just the obvious one (e.g. clear a timer ref and also null it out so the next scheduling call knows to re-arm).
- For state that should be reconciled on becoming visible again (e.g. flush buffered data, cancel in-flight async work and reflect that in the UI), make sure the cleanup leaves the component able to pick back up correctly when shown again.
- For one-time initialization/navigation logic, use a ref that persists across hide/show cycles to ensure it only fires once per successful run, while still allowing per-visit work (like refreshing data) to re-run every time.
- Add a test that mounts the component inside a real `<Activity>`, toggles visible → hidden → visible while an effect's work is in flight, and asserts both that the in-flight work is properly resolved/cancelled and that state after resuming is correct (e.g. a pending stream flush still delivers its data, a cancelled recording returns the button to "idle", a bootstrapped selection is not redone).

Example pattern:
```tsx
const timerRef = useRef<number | null>(null);
useEffect(() => {
  return () => {
    if (timerRef.current !== null) {
      clearTimeout(timerRef.current);
      timerRef.current = null; // not just cleared, but nulled so re-arming works after resume
    }
  };
}, []);

const bootstrappedRef = useRef(false); // survives hide/show, unlike state
useEffect(() => {
  loadContext().then((result) => {
    refreshData(result); // always reruns
    if (!bootstrappedRef.current) {
      bootstrappedRef.current = true;
      dispatchInitialNavigation(result); // only once, ever
    }
  });
}, []);
```