---
title: Resilient error-state handling
description: 'When an interaction or startup path can fail (or an expected event never
  arrives), make error handling deterministic and user-safe: clean up reliably, reuse
  the same validation+error messaging, recover on the right signal, and replace (not
  just cover) UI that could trap focus.'
repository: Cline/Cline
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70840
---

When an interaction or startup path can fail (or an expected event never arrives), make error handling deterministic and user-safe: clean up reliably, reuse the same validation+error messaging, recover on the right signal, and replace (not just cover) UI that could trap focus.

Apply this checklist:
1) Deterministic cleanup for missing events
- Don’t assume lifecycle events (e.g., pointerup) always fire.
- Ensure handlers restore global side effects (cursor, user-select) and remove listeners even on “release outside window” scenarios.

Example pattern:
```ts
function startDrag({ clientY }: { clientY: number }) {
  const startHeight = height;
  const previousCursor = document.body.style.cursor;
  const previousUserSelect = document.body.style.userSelect;
  document.body.style.cursor = 'row-resize';
  document.body.style.userSelect = 'none';

  const end = () => {
    document.body.style.cursor = previousCursor;
    document.body.style.userSelect = previousUserSelect;
    window.removeEventListener('pointermove', onMove);
    window.removeEventListener('pointerup', end);
    window.removeEventListener('pointercancel', end);
  };

  const onMove = (move: PointerEvent) => {
    // Cover edge cases: release outside window may skip pointerup.
    if ((move.buttons ?? 0) === 0) return end();
    onHeightChange(clampTerminalPanelHeight(startHeight + (clientY - move.clientY), window.innerHeight));
  };

  window.addEventListener('pointermove', onMove);
  window.addEventListener('pointerup', end);
  window.addEventListener('pointercancel', end);
}
```

2) Reuse the same “can send/can’t send” checks on every action path
- If there’s an alternate UI entry point (tray buttons, slash commands, one-key actions), run the composer’s existing gating checks first.
- If blocked: show the same toast/message as the main path and do not mutate drafts/attachments.

3) Retry startup/environment lookups on the real recovery boundary
- Tie retries to the correct signal (e.g., transport reconnect), not to unrelated state (e.g., signed-in account refresh).
- Add tests for “first request fails → later reconnect succeeds”.

4) On later failures, replace the UI state to prevent trapping
- If a previously mounted app can trap focus or disable pointer events, don’t just cover it with an overlay.
- Prefer replacing/unmounting the app with the failure/recovery screen, while keeping critical dialogs on top (z-order) so the user always gets a clear recovery path.