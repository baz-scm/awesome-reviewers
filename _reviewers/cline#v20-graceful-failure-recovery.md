---
title: Graceful failure recovery
description: Design for the cases where an expected completion never happens (missed
  events, timed-out requests) by adding explicit cleanup and a deterministic recovery
  trigger.
repository: cline/cline#v20
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 70886
---

Design for the cases where an expected completion never happens (missed events, timed-out requests) by adding explicit cleanup and a deterministic recovery trigger.

Apply this standard:
1) UI event lifecycles: don’t rely solely on ideal event ordering.
- Add guards for abnormal termination (e.g., release outside the window where `pointerup` never fires).
- Ensure any global side effects you set (listeners, cursor, selection, body styles) are always restored when the interaction should end.

Example (mimics the discussed fix):
```ts
const handleResizeStart = (event: ReactPointerEvent<HTMLDivElement>) => {
  if (event.button !== 0) return;
  event.preventDefault();

  const previousCursor = document.body.style.cursor;
  const previousUserSelect = document.body.style.userSelect;
  document.body.style.cursor = "row-resize";
  document.body.style.userSelect = "none";

  const startY = event.clientY;
  const startHeight = height;

  const handleMove = (move: PointerEvent) => {
    // Recovery for missed pointerup (release outside window)
    if ((move.buttons ?? 0) === 0) {
      document.body.style.cursor = previousCursor;
      document.body.style.userSelect = previousUserSelect;
      window.removeEventListener("pointermove", handleMove);
      window.removeEventListener("pointerup", handleUp);
      window.removeEventListener("pointercancel", handleUp);
      return;
    }
    onHeightChange(startHeight + (startY - move.clientY));
  };

  const handleUp = () => {
    document.body.style.cursor = previousCursor;
    document.body.style.userSelect = previousUserSelect;
    window.removeEventListener("pointermove", handleMove);
    window.removeEventListener("pointerup", handleUp);
    window.removeEventListener("pointercancel", handleUp);
  };

  window.addEventListener("pointermove", handleMove);
  window.addEventListener("pointerup", handleUp);
  window.addEventListener("pointercancel", handleUp);
};
```

2) Async/network calls: retry from the right lifecycle boundary.
- Treat initial startup requests as potentially transient failure.
- Choose a recovery trigger that truly reflects retry conditions (e.g., “transport connected/reconnected”) rather than unrelated state changes.
- Add tests for failure-then-recovery.

Example pattern (mimics the discussed approach):
```ts
useEffect(() => {
  desktopClient
    .invoke<string>("get_cline_app_base_url")
    .then(setClineAppBaseUrl)
    .catch(() => undefined);
}, [connectedTransportState]); // re-run on reconnect
```

Outcome: fewer stuck UI states, and better resilience when async operations fail temporarily; behavior becomes predictable and recoverable instead of silently broken.