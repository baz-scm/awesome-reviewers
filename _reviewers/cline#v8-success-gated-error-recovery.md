---
title: Success-Gated Error Recovery
description: When an operation can fail or an expected event may not fire, keep the
  app consistent by making state transitions success-gated, providing a safe failure
  outcome, and ensuring cleanup/recovery runs.
repository: cline/cline#v8
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70867
---

When an operation can fail or an expected event may not fire, keep the app consistent by making state transitions success-gated, providing a safe failure outcome, and ensuring cleanup/recovery runs.

Apply these rules:
1) Success-gate state/UI updates: Only detach, advance mode, or clear user input after the async call reports success.
2) Define a consistent failure state: If the operation fails, preserve the preconditions needed for recovery (e.g., keep the user’s message; don’t detach the cloud session prematurely).
3) Recover on the right retry trigger: For transient connectivity/startup issues, re-run the lookup when the transport reconnects (don’t rely on a one-time effect).
4) Ensure cleanup even on missed events: If the browser interaction can end without delivering the expected event (e.g., pointerup), proactively detect it and restore listeners/styles.

Example pattern (success-gated UI + cleanup):
```ts
async function onCommitClick() {
  if (!canCommit) return;
  const trimmed = message.trim();

  try {
    const ok = await onAction({ type: "commit", message: trimmed, push });
    if (ok) setMessage(""); // only clear on success
  } catch {
    // do nothing: keep message visible so the user can retry
  }
}
```

Example pattern (retry on reconnect):
```ts
useEffect(() => {
  void desktopClient
    .invoke<string>("get_cline_app_base_url")
    .then(setClineAppBaseUrl)
    .catch(() => undefined);
}, [transportConnectedState]); // reruns after reconnect
```

This standard prevents inconsistent states (stale attachments, lost user input, stuck UI) and improves resilience to real-world failure scenarios.