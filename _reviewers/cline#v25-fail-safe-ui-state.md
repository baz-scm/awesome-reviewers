---
title: Fail-safe UI State
description: 'Ensure UI state transitions and side-effect cleanup happen correctly
  in error/edge paths. Two practical rules:


  1) Apply “success-only” state changes

  - For async actions that can fail, have the action return an explicit success indicator
  (e.g., `boolean`).'
repository: cline/cline#v25
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 70891
---

Ensure UI state transitions and side-effect cleanup happen correctly in error/edge paths. Two practical rules:

1) Apply “success-only” state changes
- For async actions that can fail, have the action return an explicit success indicator (e.g., `boolean`).
- Update user-visible state (e.g., clearing messages, closing dialogs) only when the action succeeds; preserve inputs on failure.

2) Defend against missing lifecycle events
- If you rely on browser events (drag, pointer capture, focus changes), add termination logic for abnormal paths where the expected event may never fire.
- Always restore side effects (event listeners, body styles, cursors) when ending the interaction, including in those abnormal paths.

Example pattern (combined):

```ts
// 1) success-only UI update
async function onAction(action): Promise<boolean> {
  try {
    await hostDo(action);
    return true;
  } catch {
    return false;
  }
}

async function commit() {
  const ok = await onAction({ type: "commit", message });
  if (!ok) return;           // keep message for user retry
  setMessage("");           // only on success
}

// 2) fail-safe interaction termination
function startDrag() {
  const onMove = (e: PointerEvent) => {
    // fail-safe: if button is no longer held, end drag even if pointerup never arrived
    if (e.buttons === 0) {
      endDrag();
      return;
    }
    // normal drag logic...
  };

  const endDrag = () => {
    window.removeEventListener("pointermove", onMove);
    // restore body cursor/userSelect, etc.
  };

  window.addEventListener("pointermove", onMove);
}
```

Adopting this prevents stuck interactions and avoids incorrect “success” UI after failures—directly improving robustness and error recovery.