---
title: Failure-Boundary Handling
description: 'When code involves async work, external resources, or event-driven UI,
  make failure behavior explicit: only perform destructive cleanup/state transitions
  after success; preserve user-visible state on failure; add defensive cleanup for
  missing events; and recover from startup/network failures by retrying at the correct
  lifecycle boundary (e.g., transport...'
repository: cline/cline#v12
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70872
---

When code involves async work, external resources, or event-driven UI, make failure behavior explicit: only perform destructive cleanup/state transitions after success; preserve user-visible state on failure; add defensive cleanup for missing events; and recover from startup/network failures by retrying at the correct lifecycle boundary (e.g., transport reconnect).

How to apply:
- Success-only state changes: If a UI state change depends on an async operation, update it only after that operation resolves successfully; otherwise keep the previous state (e.g., don’t clear commit input if the commit fails).
- Resource cleanup after successful prerequisites: If you must detach/close an external session, do it only after the resume/restore step succeeds; if the restore fails, leave the session attached or handle reattachment deterministically.
- Event-loss defensive cleanup: For drag/gesture logic, ensure you restore listeners/styles even if the expected “end” event never fires (e.g., window release outside sends no pointerup). End the interaction when detecting an invalid/terminal condition.
- Recovery via lifecycle-bound retries: For initialization or environment discovery calls, retry when the relevant connection/transport state changes rather than relying on a single attempt.

Example (success-only mutation + cleanup timing):
```ts
async function resume(sessionId: string) {
  // Detach only after local restore succeeds
  detachCloudSession(); // ❌ avoid this if restore can fail
}

async function resume(sessionId: string) {
  try {
    // First restore locally
    await onResumeSession(sessionId);
    // Then detach safely
    detachCloudSession();
  } catch (e) {
    // Leave external session attached (or reattach) so the user isn't stranded
    throw e;
  }
}
```

Example (preserve UI input on failure):
```ts
const commit = useCallback(async () => {
  if (!canCommit) return;
  const ok = await onAction({ type: "commit", message: message.trim(), push });
  if (ok) setMessage(""); // ✅ only clear on success
}, [canCommit, message, onAction]);
```