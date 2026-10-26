---
title: Graceful Async Failure Handling
description: When async work or UI events can fail or “never complete,” ensure your
  code keeps state consistent, gates side effects on success, retries transient startup
  work on reconnection, and performs deterministic cleanup to prevent stuck UI.
repository: cline/cline#v30
label: Error Handling
language: TSX
comments_count: 4
repository_stars: 70894
---

When async work or UI events can fail or “never complete,” ensure your code keeps state consistent, gates side effects on success, retries transient startup work on reconnection, and performs deterministic cleanup to prevent stuck UI.

**Do**
- **Gate side effects on success**: update/detach/clear UI only after the awaited operation succeeds.
- **Preserve state on failure**: if an action rejects (e.g., commit/resume), keep the user-visible state so users can retry or inspect.
- **Add retry points for transient failures**: for startup/sidecar/transport-dependent lookups, re-run when the transport reconnects instead of relying on a one-time request.
- **Defensively clean up UI/input flows**: if the “terminal” event might be missed (e.g., pointerup outside window), end the interaction when detecting an invalid condition (e.g., button no longer held) and restore styles/listeners.

**Pattern (success-gated + retry-friendly)**
```ts
// Success-gated state transition
async function resume(sessionId: string) {
  // DO NOT detach/commit irreversible state until restore succeeds
  const result = await localRestore(sessionId);
  if (!result.ok) return; // keep cloud attached / keep UI intact
  detachCloudSession();
}

// Retry on reconnection (transport-dependent lookup)
useEffect(() => {
  // run on each reconnect/transport state change
  if (!transport.connected) return;
  lookupBaseUrl()
    .then(setBaseUrl)
    .catch(() => {
      // leave existing UI; next reconnect will retry
    });
}, [transport.connected]);

// Deterministic cleanup for missed terminal events
function onMove(e: PointerEvent) {
  if (e.buttons === 0) {
    // treat as an ended drag: restore styles + remove listeners
    cleanupDrag();
    return;
  }
  // ...normal move handling...
}
```

This prevents partial failure states like “detached too early,” lost user input after a rejected operation, broken links after a transient startup timeout, and stuck pointer/UI behavior.