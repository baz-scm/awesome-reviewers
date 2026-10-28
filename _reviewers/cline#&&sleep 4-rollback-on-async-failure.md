---
title: Rollback on async failure
description: When an async operation can fail after the UI has optimistically applied
  a state change (e.g., switching modes, detaching a session, resuming work), always
  catch the rejection and restore the previous consistent state rather than letting
  the error propagate unhandled. Order side effects so that any irreversible action
  (detaching, discarding, committing)...
repository: cline/cline#&&sleep 4
label: Error Handling
language: TSX
comments_count: 3
repository_stars: 70980
---

When an async operation can fail after the UI has optimistically applied a state change (e.g., switching modes, detaching a session, resuming work), always catch the rejection and restore the previous consistent state rather than letting the error propagate unhandled. Order side effects so that any irreversible action (detaching, discarding, committing) only happens after the async step it depends on has succeeded, not before. For fire-and-forget actions where no meaningful recovery is possible (e.g., opening an external URL), it's acceptable to swallow the error with a no-op catch, but document why, and do not silently swallow errors for actions that affect shared app state.

Example:
```ts
const toggleMode = useCallback(() => {
  const previousMode = session.uiMode;
  const newMode = previousMode === "act" ? "plan" : "act";
  session.toggleMode();
  // The switch restarts the session runtime; if that fails, the runtime is
  // still in the previous mode, so revert the UI instead of letting the
  // rejection escape and crash the app.
  props.onModeChange(newMode).catch((error: unknown) => {
    session.setUiMode(previousMode);
    showToast(`Failed to switch mode: ${String(error)}`);
  });
}, [props, session]);

const resumeSession = useCallback(
  async (sessionId: string) => {
    const result = await propsOnResumeSession(sessionId);
    // Only detach the cloud session once the local resume actually succeeds;
    // detaching first would strand the chat if the resume fails.
    detachCloudSession();
    return result;
  },
  [propsOnResumeSession, detachCloudSession],
);
```