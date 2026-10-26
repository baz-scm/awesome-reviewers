---
title: Resilient UI Error Recovery
description: 'Design UI flows so they can recover from failures and tolerate missed/ambiguous
  signals (failed async startup, lost pointer events, or inputs that don’t reflect
  user intent). Concretely:'
repository: cline/cline#v16
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70882
---

Design UI flows so they can recover from failures and tolerate missed/ambiguous signals (failed async startup, lost pointer events, or inputs that don’t reflect user intent). Concretely:

- Retry on real recovery triggers (not user/account refresh): if an async lookup can fail during startup, re-run it when the underlying transport reconnects or the relevant external environment changes.
- Ensure teardown happens even if the expected end event never arrives: for drag/resize, add a termination condition that detects “release without pointerup” and restores listeners/body styles.
- Separate user intent from programmatic updates and ignore irrelevant inputs: track a “target” (e.g., programmatic scroll destination) or check event scope (e.g., only respond to key events when the event target is the intended viewport) so edge cases don’t permanently unpin/lock/stick UI state.

Example patterns:

```ts
// 1) Async recovery on reconnect
useEffect(() => {
  desktopClient
    .invoke<string>('get_cline_app_base_url')
    .then(setClineAppBaseUrl)
    .catch(() => undefined);
}, [/* connected transport state */]);

// 2) Drag teardown even when pointerup is missed
const onPointerMove = (e: PointerEvent) => {
  if (!e.buttons) {
    // release detected; cleanup listeners + restore styles
    cleanupDrag();
    return;
  }
  updateHeightFromDelta(e);
};

// 3) Intent-based state updates
const handleScroll = () => {
  // Ignore scroll events caused by your own action until arrival,
  // then clear the target; otherwise user un-pin/pin logic stays correct.
  if (ourScrollTarget.current !== null) {
    const arrived = Math.abs(viewport.scrollTop - ourScrollTarget.current) <= 1;
    if (!arrived) return;
    ourScrollTarget.current = null;
  }
  setPinned(distanceFromBottom(viewport) <= PINNED_THRESHOLD_PX);
};
```

Apply this as a standard when adding event-driven interactions and async initialization: assume the happy path won’t always deliver the “done” signal, and ensure the component either cleans up or self-corrects on the next reliable state change.