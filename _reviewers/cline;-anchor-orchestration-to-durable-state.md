---
title: Anchor orchestration to durable state
description: Long-running or multi-step workflows must not depend on a transient client/viewer
  connection to complete safely. If orchestration state (e.g., "which branch was pushed",
  "which client owns this capability") lives only in an ephemeral process or in-memory
  map tied to a short-lived connection, a disconnect at the wrong moment can leave
  the workflow half-done...
repository: cline/cline;
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 70964
---

Long-running or multi-step workflows must not depend on a transient client/viewer connection to complete safely. If orchestration state (e.g., "which branch was pushed", "which client owns this capability") lives only in an ephemeral process or in-memory map tied to a short-lived connection, a disconnect at the wrong moment can leave the workflow half-done (e.g., a branch pushed with no task created) or cause requests to be routed to a client that is no longer actually participating, leading to duplicate side effects or stalled retries.

To avoid this:
- Perform state-mutating steps (git push, task creation, initial send, etc.) in the durable server/orchestrator (e.g., the Hub/core process) rather than splitting them across a client that may disappear mid-sequence. The client should only prepare and hand off the data needed; the server completes the sequence atomically from its own durable context.
- When resuming or routing work to a participant (e.g., picking a client to answer a capability request), only select participants that are verified to still be actively attached (e.g., tracked in a maintained `participants`/`attached` set), not just "currently connected." Stale or detached entries must be pruned or skipped.
- If no valid active participant exists, fail fast with a clear error rather than silently waiting indefinitely or picking a stale candidate.
- Add end-to-end tests that simulate the disconnect/reconnect and multi-participant scenarios (e.g., quitting and reopening a client while the server keeps running, or owner-detaches-then-another-joins) to confirm the workflow completes correctly and doesn't duplicate work.

Example of the ownership-resolution pattern:
```ts
function resolveCapabilityOwner(ctx, sessionId, capabilityName, targetClientId) {
  if (ctx.clients.has(targetClientId) && ctx.sessionState.participants.has(targetClientId)) {
    return targetClientId;
  }
  return ctx.capabilityClientsBySession
    ?.get(sessionId)
    ?.get(capabilityName)
    ?.find((clientId) =>
      ctx.clients.has(clientId) && ctx.sessionState.participants.has(clientId)
    );
}
```
This ensures routing only targets clients that are both connected and still attached to the task, preventing requests from going to clients that detached but remained technically connected.</description>
</invoke>
