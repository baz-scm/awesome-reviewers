---
title: Safe async state transitions
description: When triggering async operations that can fail, never let a rejection
  escape unhandled, and never commit a dependent state change before the async operation
  has actually succeeded. For truly fire-and-forget calls (e.g. opening an external
  link), attach a no-op `.catch(() => {})` so a failure can't crash the app, since
  there's no state to roll back. For...
repository: cline/cline#;sleep 4;
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70976
---

When triggering async operations that can fail, never let a rejection escape unhandled, and never commit a dependent state change before the async operation has actually succeeded. For truly fire-and-forget calls (e.g. opening an external link), attach a no-op `.catch(() => {})` so a failure can't crash the app, since there's no state to roll back. For operations that change application state (e.g. switching modes, detaching a session) as a side effect of an async call, defer the side effect until the async call resolves successfully; on failure, catch the error, surface it to the user if appropriate, and roll the UI/state back using the authoritative source of truth (e.g. `props.config.mode`) rather than a captured local variable, to avoid stale or inconsistent state.

Example:
```ts
const toggleMode = useCallback(() => {
  const previousMode = session.uiMode;
  const newMode = previousMode === "act" ? "plan" : "act";
  session.toggleMode();
  props.onModeChange(newMode).catch((error: unknown) => {
    // Roll back optimistic UI change and resync from authoritative config
    session.setUiMode(previousMode);
    showToast(`Failed to switch mode: ${error}`);
  });
}, [props, session]);
```
and for irreversible side effects like detaching a cloud session, perform the detach only after the local resume succeeds:
```ts
const resumeSession = useCallback(async (sessionId: string) => {
  const result = await propsOnResumeSession(sessionId);
  detachCloudSession(); // only detach once the restore has succeeded
  return result;
}, [propsOnResumeSession, detachCloudSession]);
```