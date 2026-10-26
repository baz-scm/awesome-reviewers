---
title: Handle Async Failures
description: When an operation depends on async work (commits, runtime restarts, initialization/sidecar
  calls, hub readiness), handle failure explicitly and recover the UI to a known-good
  state.
repository: cline/cline#v15
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70877
---

When an operation depends on async work (commits, runtime restarts, initialization/sidecar calls, hub readiness), handle failure explicitly and recover the UI to a known-good state.

Apply this standard:
1) **Catch and contain async rejections** in UI/event handlers so failures don’t take down the app.
2) **Rollback or preserve prior state on failure** (mode/config/UI toggles) and avoid leaving “optimistic” UI in a broken state.
3) **Commit side effects only on success** (e.g., clear success-only messages/forms only after the promise resolves).
4) **Retry initialization on reconnect/transport readiness** when failures are transient (sidecar/hub/app-base-url lookups).
5) **Gate critical mounts on dependency readiness**; if readiness later fails, **swap** to a safe fallback screen instead of covering an invalid UI.

Example pattern (rollback + success-only side effects):
```ts
const previous = session.uiMode;
const newMode = previous === "act" ? "plan" : "act";

session.toggleMode();
props.onModeChange(newMode).catch((err) => {
  // restore known-good config/UI
  session.setUiMode(previous);
  // optionally show an error toast/dialog here
});
```
And example pattern (success-only UI update):
```ts
async function commit(push: boolean) {
  if (!canCommit) return;
  try {
    await onAction({ type: "commit", message: message.trim(), push });
    setMessage(""); // only after success
  } catch {
    // keep message so the user can retry
  }
}
```

This reduces cascaded failures and ensures users can recover without refreshing or getting stuck in a broken/frozen UI state.