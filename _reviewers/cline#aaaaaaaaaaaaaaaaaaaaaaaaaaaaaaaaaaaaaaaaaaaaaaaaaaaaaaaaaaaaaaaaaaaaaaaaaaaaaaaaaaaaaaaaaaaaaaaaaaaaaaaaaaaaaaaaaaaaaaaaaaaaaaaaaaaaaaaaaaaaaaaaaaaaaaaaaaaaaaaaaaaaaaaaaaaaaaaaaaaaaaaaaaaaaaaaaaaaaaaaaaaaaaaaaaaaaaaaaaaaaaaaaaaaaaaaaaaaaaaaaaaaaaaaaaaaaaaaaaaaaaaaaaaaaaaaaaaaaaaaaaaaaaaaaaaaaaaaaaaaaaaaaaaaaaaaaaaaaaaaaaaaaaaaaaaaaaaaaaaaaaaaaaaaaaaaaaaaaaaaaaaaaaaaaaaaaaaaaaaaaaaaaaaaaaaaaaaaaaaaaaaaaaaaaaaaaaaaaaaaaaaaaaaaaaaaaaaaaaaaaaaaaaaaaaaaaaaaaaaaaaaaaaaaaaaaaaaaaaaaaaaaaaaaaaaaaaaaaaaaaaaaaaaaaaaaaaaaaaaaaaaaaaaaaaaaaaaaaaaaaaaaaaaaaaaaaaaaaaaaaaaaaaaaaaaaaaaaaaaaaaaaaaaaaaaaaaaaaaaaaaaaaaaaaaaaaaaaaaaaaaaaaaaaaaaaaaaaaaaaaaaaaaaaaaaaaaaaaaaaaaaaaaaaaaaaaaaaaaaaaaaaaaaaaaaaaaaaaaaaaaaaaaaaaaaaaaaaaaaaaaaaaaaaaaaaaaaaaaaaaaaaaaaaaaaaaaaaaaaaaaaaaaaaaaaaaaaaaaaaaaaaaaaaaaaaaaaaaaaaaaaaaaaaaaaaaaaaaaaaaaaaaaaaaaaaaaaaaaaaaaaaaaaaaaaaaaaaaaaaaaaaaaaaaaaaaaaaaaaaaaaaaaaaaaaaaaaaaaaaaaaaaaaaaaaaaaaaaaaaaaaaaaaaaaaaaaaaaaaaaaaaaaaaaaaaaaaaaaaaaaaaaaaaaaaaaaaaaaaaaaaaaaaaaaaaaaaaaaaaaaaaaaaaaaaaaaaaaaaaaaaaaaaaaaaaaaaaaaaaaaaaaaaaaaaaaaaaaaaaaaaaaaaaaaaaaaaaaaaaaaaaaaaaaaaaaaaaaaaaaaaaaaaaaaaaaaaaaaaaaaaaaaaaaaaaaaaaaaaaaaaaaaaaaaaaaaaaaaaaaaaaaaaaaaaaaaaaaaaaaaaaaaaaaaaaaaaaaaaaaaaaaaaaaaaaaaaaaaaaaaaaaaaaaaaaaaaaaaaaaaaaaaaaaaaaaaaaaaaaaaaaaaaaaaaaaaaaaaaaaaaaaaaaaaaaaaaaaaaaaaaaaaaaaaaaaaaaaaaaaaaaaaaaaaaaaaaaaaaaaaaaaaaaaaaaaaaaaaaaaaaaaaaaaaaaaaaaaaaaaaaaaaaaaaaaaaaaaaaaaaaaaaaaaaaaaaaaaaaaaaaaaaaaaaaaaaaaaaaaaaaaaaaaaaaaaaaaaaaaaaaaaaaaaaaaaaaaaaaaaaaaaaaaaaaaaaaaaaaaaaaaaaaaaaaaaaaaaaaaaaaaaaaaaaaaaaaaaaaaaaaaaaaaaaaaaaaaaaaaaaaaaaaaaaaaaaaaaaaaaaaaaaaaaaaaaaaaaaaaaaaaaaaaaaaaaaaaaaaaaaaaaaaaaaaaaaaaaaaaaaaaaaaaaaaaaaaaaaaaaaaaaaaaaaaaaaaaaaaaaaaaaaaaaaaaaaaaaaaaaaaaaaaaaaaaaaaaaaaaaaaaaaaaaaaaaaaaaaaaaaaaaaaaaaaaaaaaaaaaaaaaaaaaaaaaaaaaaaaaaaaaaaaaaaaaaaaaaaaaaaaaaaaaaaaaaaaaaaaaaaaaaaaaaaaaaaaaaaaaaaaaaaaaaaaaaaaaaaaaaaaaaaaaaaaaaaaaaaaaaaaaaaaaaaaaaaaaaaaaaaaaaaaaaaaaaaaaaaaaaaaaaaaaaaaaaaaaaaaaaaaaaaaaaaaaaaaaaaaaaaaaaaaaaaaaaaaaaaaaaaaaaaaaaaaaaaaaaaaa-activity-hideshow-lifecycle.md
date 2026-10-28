---
title: Activity hide/show lifecycle
description: Prefer hiding expensive subtrees with React's `<Activity>` (or an equivalent
  keep-alive wrapper) over unmounting/remounting them when a dependency (e.g. a backend
  connection) becomes temporarily unavailable. This preserves component state—open
  conversations, selected items, form drafts—across a reconnect, and properly tears
  down portaled dialogs/popovers...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: React
language: TSX
comments_count: 5
repository_stars: 70965
---

Prefer hiding expensive subtrees with React's `<Activity>` (or an equivalent keep-alive wrapper) over unmounting/remounting them when a dependency (e.g. a backend connection) becomes temporarily unavailable. This preserves component state—open conversations, selected items, form drafts—across a reconnect, and properly tears down portaled dialogs/popovers (releasing focus traps and `pointer-events` locks) that a simple CSS-overlay approach would leave dangling.

However, hiding is not a true unmount: effects re-run their setup when the subtree becomes visible again, so any "unmount-only" cleanup that only clears a timer or ref without resetting the associated boolean/state flag will leave the component in a stale, inconsistent state after it resumes (e.g. a stream-flush scheduler that never re-arms, or a "recording" flag stuck `true` after the underlying operation was actually cancelled). Audit every cleanup function in a hideable subtree and make sure it fully resets state, not just side effects, so re-running setup produces a consistent starting point:

```ts
useEffect(() => {
  return () => {
    clearTimeout(timerRef.current);
    timerRef.current = null; // not just clearing the timer—resetting the flag too
  };
}, []);
```

Likewise, any "run once" bootstrap effect (e.g. initial navigation/selection logic) must use a ref—not component state—to track whether it already ran, since the ref survives a hide/show cycle while still allowing non-bootstrap parts of the effect (like refreshing data) to re-run on every visibility change:

```ts
const bootstrapped = useRef(false);
useEffect(() => {
  loadContext().then((ctx) => {
    refreshEnvironment(ctx); // always re-run
    if (!bootstrapped.current) {
      bootstrapped.current = true;
      dispatch(selectDefaultDraft()); // only once, ever
    }
  });
}, [trigger]);
```

When adding a hide/show capable component, add a test that explicitly toggles visibility mid-operation (a pending timer, an in-flight async call, an active recording) and asserts the component resumes correctly—this is the class of bug that slips through otherwise.