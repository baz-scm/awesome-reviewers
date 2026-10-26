---
title: Deterministic Failure Recovery
description: Treat every async/session/interactive flow as having explicit failure
  recovery. Ensure that on failure (or missing “success” signals), the app transitions
  to a known state and can recover without manual refresh.
repository: cline/cline#v26
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70893
---

Treat every async/session/interactive flow as having explicit failure recovery. Ensure that on failure (or missing “success” signals), the app transitions to a known state and can recover without manual refresh.

Practical checklist:
1) Gate state transitions on success
- Only clear UI inputs, advance state, or detach/stop sending to external services after the awaited operation truly succeeds.

2) Tie retries to the real retry boundary
- If recovery depends on reconnect/re-subscribe (sidecar/hub transport), make the lookup/retry effect depend on the connection/reconnect state—not on unrelated state like “current account” or an optimistic refresh.

3) Add defensive cleanup for missing events
- For pointer/drag/session lifecycles, assume events may not fire (e.g., pointerup outside window). Detect alternative signals (e.g., button not held) and restore listeners/styles/flags.

4) Replace risky UI on failure, don’t just cover it
- When a failure state must prevent focus traps or pointer-event issues, unmount/replace the underlying interactive surface rather than relying on inert/overlay behavior. Keep critical dialogs layered above.

Example pattern (success-gated async + safe teardown):
```ts
const onPrimary = useCallback(async () => {
  // optimistic UI changes avoided
  const ok = await doAsyncAction();
  if (!ok) {
    // keep user input / leave session attached
    return;
  }
  // mutate UI state only after success
  setMessage("");
  detachCloudSession();
}, [/* deps */]);

useEffect(() => {
  // Defensive cleanup in case expected events never arrive
  const onMove = (e: PointerEvent) => {
    if (e.buttons === 0) endDrag();
  };
  window.addEventListener("pointermove", onMove);
  return () => window.removeEventListener("pointermove", onMove);
}, []);
```