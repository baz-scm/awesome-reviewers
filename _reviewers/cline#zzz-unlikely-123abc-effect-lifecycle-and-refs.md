---
title: Effect lifecycle and refs
description: 'When a component can be hidden/shown without unmounting (e.g. wrapped
  in `<Activity>`, kept alive across session switches, or driven by a connection/startup
  state machine), audit every effect for what should happen on each resume: bootstrap-once
  effects must guard with a `useRef` flag that is set only after a genuine success
  (not on every mount, since refs...'
repository: cline/cline#zzz-unlikely-123abc
label: React
language: TSX
comments_count: 5
repository_stars: 71035
---

When a component can be hidden/shown without unmounting (e.g. wrapped in `<Activity>`, kept alive across session switches, or driven by a connection/startup state machine), audit every effect for what should happen on each resume: bootstrap-once effects must guard with a `useRef` flag that is set only after a genuine success (not on every mount, since refs persist across hides), while effects that arm a timer or other resumable resource must reset their guard ref in cleanup so the resume path can re-arm it. Don't let a "run once" effect silently become "run once ever" when it should be "run once per successful load," and don't let a "re-arm on each effect run" cleanup leave a stale `null`/sentinel that blocks future scheduling.

Similarly, avoid inferring a semantic state transition (a new turn started, a message was sent, a run is in flight) from an indirect derived value like a message/count comparison — these are fragile to off-by-one and history-hydration edge cases. Instead, track transitions explicitly: bump a ref-based epoch/generation counter when the real event occurs, or have the owning hook/caller pass the actual semantic signal (e.g. `isSessionSwitching`) down as a prop instead of asking the consumer to reverse-engineer it from state shape.

Example pattern for bootstrap-once-per-success across resumes:
```tsx
function useRemoteEnvironmentBootstrap(environmentId: string) {
  const bootstrappedRef = useRef(false); // survives Activity hide/show

  useEffect(() => {
    let cancelled = false;
    getProcessContext(environmentId).then((ctx) => {
      if (cancelled) return;
      refreshActiveEnvironment(ctx); // always refresh on every successful load
      if (!bootstrappedRef.current) {
        bootstrappedRef.current = true;
        dispatch({ type: "select-environment-draft", environmentId });
      }
    });
    return () => { cancelled = true; };
  }, [environmentId]);
}
```
And for a cleanup that must allow re-arming on resume:
```tsx
useEffect(() => {
  return () => {
    if (flushTimerRef.current !== null) {
      clearTimeout(flushTimerRef.current);
      flushTimerRef.current = null; // without this, schedulePendingFlush() thinks a timer is still pending after resume
    }
  };
}, []);
```
Write a regression test that exercises the actual hide/show (or reconnect) cycle rather than only the happy path, since these bugs only surface on the second mount/resume.