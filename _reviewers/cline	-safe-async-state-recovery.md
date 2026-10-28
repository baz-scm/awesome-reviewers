---
title: Safe async state recovery
description: When an operation performs an optimistic state change and then triggers
  an async side effect (RPC call, session restart, cross-system sync), do not finalize
  dependent state until that async call actually succeeds. If the call fails, catch
  the rejection, roll back to the last known-good state, and surface the failure instead
  of letting the exception...
repository: "cline/cline\t"
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70947
---

When an operation performs an optimistic state change and then triggers an async side effect (RPC call, session restart, cross-system sync), do not finalize dependent state until that async call actually succeeds. If the call fails, catch the rejection, roll back to the last known-good state, and surface the failure instead of letting the exception propagate uncaught (which can crash the UI or leave the app in an inconsistent state). Likewise, guard against performing destructive or stateful actions when preconditions aren't met (e.g. applying a local-only action to a cloud-backed session), and tie automatic retries to the signal that actually indicates recovery is possible (e.g. retry on reconnect rather than on an unrelated trigger).

Example pattern:
```ts
const toggleMode = useCallback(() => {
  const previousMode = session.uiMode;
  const newMode = previousMode === "act" ? "plan" : "act";
  session.toggleMode(); // optimistic UI update

  props.onModeChange(newMode).catch((error: unknown) => {
    // Restart failed — the runtime is still in previousMode, so revert
    // the UI and surface the error instead of letting it escape.
    session.setUiMode(previousMode);
    showToast(`Failed to switch mode: ${error}`);
  });
}, [props, session]);
```

Apply the same discipline to detach/attach, resume, or reconnect flows: only detach/replace a resource once the replacement has been confirmed to succeed, and validate operation preconditions before performing state-changing actions to avoid producing an incorrect or unrecoverable state on failure.