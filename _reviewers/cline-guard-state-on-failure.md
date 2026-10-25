---
title: Guard state on failure
description: When an action can fail or an environment can change, ensure error handling
  preserves user state, prevents incorrect side effects, and recovers automatically.
repository: cline/CLINE
label: Error Handling
language: TSX
comments_count: 5
repository_stars: 70839
---

When an action can fail or an environment can change, ensure error handling preserves user state, prevents incorrect side effects, and recovers automatically.

Apply this checklist:
1) Pre-flight validations before mutation
- Run the same “send/commit/resume” checks the primary path uses.
- If blocked, show the expected UI feedback (toast/message) and leave drafts/attachments unchanged.

2) Only transition/cleanup after success is confirmed
- Avoid premature detachment, clearing text, or switching modes until the async operation reports success.
- If you need cleanup (e.g., detaching a session), do it only after the local restore/commit/send truly succeeds.

3) Restore UI/event side effects on all exit paths
- For drag-like handlers, handle “unexpected” termination (e.g., release outside the window, missing pointerup) by ending the drag and restoring body styles/listeners.

4) Implement recovery for transient failures
- For startup/network/sidecar lookups, re-run the failing request when transport connectivity changes (reconnect) rather than relying on a one-time effect.

5) Test failure scenarios explicitly
- Add tests that assert state is preserved after failure (e.g., message not cleared, draft still present, session not detached prematurely, link appears after reconnect).

Example pattern (state changes only after success):

```ts
async function onCommit() {
  // pre-flight checks
  if (!canCommit) return;

  const ok = await onAction({ type: "commit", message: trimmed, push });
  if (ok) setMessage(""); // only clear on success
}
```

```ts
async function onResume(sessionId: string) {
  // If resume fails, keep the remote/cloud session attached.
  const ok = await localRestore(sessionId);
  if (ok) detachCloudSession();
}
```