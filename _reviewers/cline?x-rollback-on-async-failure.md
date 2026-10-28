---
title: Rollback on async failure
description: 'Several bugs shared the same root cause: code assumed an async operation
  (session resume, mode switch, commit, send) would succeed and mutated shared state
  immediately, before the operation actually resolved. When the operation failed,
  the UI was left desynced, data was lost, or the app crashed with an unhandled rejection.'
repository: cline/cline?x
label: Error Handling
language: TSX
comments_count: 6
repository_stars: 70983
---

Several bugs shared the same root cause: code assumed an async operation (session resume, mode switch, commit, send) would succeed and mutated shared state immediately, before the operation actually resolved. When the operation failed, the UI was left desynced, data was lost, or the app crashed with an unhandled rejection.

Apply this rule whenever triggering an async action that can fail:
1. Do not perform destructive or state-detaching side effects (detaching a session, clearing a draft/input, disabling a control) until the async call has resolved successfully. If the action fails, the pre-action state should still be intact.
2. Always attach a `.catch`/try-catch to async calls that cross a boundary the caller doesn't fully control (restarting a runtime, network calls, IPC). Never let a rejection escape uncaught and take down the whole app.
3. On failure, roll back to the actual, confirmed source of truth (e.g. `props.config.mode`) rather than a value captured before the call started — this prevents two overlapping failures from reverting to the wrong state.
4. Validate/guard conditions (read-only mode, missing model, unsupported input) in one shared path so every trigger (keyboard shortcut, button, suggestion tray, etc.) enforces the same checks and gives the same user-facing error, instead of letting some entry points skip validation.
5. Where the completion signal might never fire (e.g. a `pointerup` outside the window), add a fallback detection path so cleanup still runs and the app doesn't end up in a stuck/inconsistent state.

Example pattern:
```ts
const previous = session.uiMode;
session.setUiMode(nextMode); // optimistic UI update

onModeChange(nextMode).catch((error) => {
  // Roll back to the confirmed state, not a stale capture
  session.setUiMode(props.config.mode);
  showToast(`Failed to switch mode: ${error.message}`);
});
```
and for UI that only "commits" on success:
```ts
const committed = await onAction({ type: "commit", message });
if (committed) setMessage(""); // only clear on confirmed success
```

Following this pattern keeps the UI consistent with real backend state, preserves user input on failure, and prevents unhandled rejections from crashing the application.