---
title: Revert optimistic state safely
description: When an async operation can fail after the UI has already applied an
  optimistic update, always attach a rejection handler and reconcile the UI back to
  the authoritative source of truth rather than letting the error propagate unhandled
  or leaving the UI in an inconsistent state. Reverting to a value captured before
  the call can be wrong if a second operation...
repository: cline/cline
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70886
---

When an async operation can fail after the UI has already applied an optimistic update, always attach a rejection handler and reconcile the UI back to the authoritative source of truth rather than letting the error propagate unhandled or leaving the UI in an inconsistent state. Reverting to a value captured before the call can be wrong if a second operation started in the meantime; instead resync from the actual backend/config state once the failure is known.

Example:
```ts
const toggleMode = useCallback(() => {
  const newMode = session.uiMode === "act" ? "plan" : "act";
  session.toggleMode(); // optimistic UI update
  props.onModeChange(newMode).catch((error: unknown) => {
    // Don't restore a captured "previous" value — resync to the real
    // runtime state, since another toggle may have changed it meanwhile.
    session.setUiMode(props.config.mode);
    showError(error);
  });
}, [props, session]);
```

Additionally, tie any retry/recovery logic to the event that actually governs the failing resource (e.g. retry a lookup on transport reconnect rather than an unrelated refresh trigger), and before auto-recovering user data (e.g. restoring a draft after a failed send), confirm the operation definitely did not complete — don't apply blanket recovery when the outcome is uncertain, since that can silently drop edits or duplicate state. Always cover these paths with a regression test that forces the failure and asserts the UI/state ends up consistent with the real backend state.