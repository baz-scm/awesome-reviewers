---
title: Async failure rollback
description: When an async operation drives a state transition (UI mode, session attachment,
  resumed task, etc.), do not commit the new state optimistically before the operation
  succeeds, and never let its rejection escape unhandled. Catch the failure, restore
  the previously known-good state, and resync indicators from the source of truth
  rather than a captured value....
repository: cline/cline#$(sleep 4)
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70978
---

When an async operation drives a state transition (UI mode, session attachment, resumed task, etc.), do not commit the new state optimistically before the operation succeeds, and never let its rejection escape unhandled. Catch the failure, restore the previously known-good state, and resync indicators from the source of truth rather than a captured value. For example, when toggling a mode that restarts a runtime, keep the previous mode and roll back on failure instead of leaving the UI out of sync with the actual config:

```ts
props.onModeChange(newMode).catch((error) => {
  session.setUiMode(previousMode);
  applyInteractiveModeConfig(previousMode);
  showToast("Failed to switch mode");
});
```

Similarly, only detach a cloud session after a local resume has actually succeeded, so a failed resume doesn't strand the session in neither state. For transient failures in one-shot async lookups (e.g., a sidecar call at startup), wire retries to the appropriate lifecycle event (such as reconnect) rather than an unrelated trigger. For deliberate fire-and-forget actions (e.g., opening an external link) where failure is non-critical and has no useful recovery path, swallow the error explicitly with a comment explaining why, so it's clear the omission is intentional rather than an oversight.