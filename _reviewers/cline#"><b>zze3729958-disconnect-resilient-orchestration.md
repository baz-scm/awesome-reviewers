---
title: Disconnect-resilient orchestration
description: Long-running, multi-step workflows (task creation, session runs, callback
  handling) must not depend on a single client connection staying alive for the whole
  duration. Keep orchestration state and in-flight step tracking in a durable layer
  (e.g. a hub/core process) rather than in per-connection memory such as a WeakMap
  scoped to the local app, so a step...
repository: cline/cline#"><b>zze3729958
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 71067
---

Long-running, multi-step workflows (task creation, session runs, callback handling) must not depend on a single client connection staying alive for the whole duration. Keep orchestration state and in-flight step tracking in a durable layer (e.g. a hub/core process) rather than in per-connection memory such as a WeakMap scoped to the local app, so a step sequence like "push branch → create task → send initial message" can complete even if the initiating client closes mid-sequence. Any side effect that could be retried (e.g. a git push) must be idempotent or resumable instead of blindly re-executed, to avoid duplicated branches/tasks when a retry happens after a partial failure.

For signals/callbacks tied to a specific client, don't let the whole workflow die just because the original owner disconnected: route the next callback to another live party that is already registered for the same task (and add a test asserting failover), rather than tying the callback exclusively to the first client. Likewise, when a client attempts to "start" a run that is already in progress, reattach to the live run instead of silently replacing it—replacing it leaves the old run unreachable (no way to abort or enqueue into it) and causes subsequent writes to land on a stale snapshot. Document any gaps (e.g. "doesn't protect against a crash of the durable layer itself, only against the viewer disconnecting") so remaining failure modes are explicit and testable.

Example pattern to apply:
```ts
const live = this.sessions.get(sessionId);
if (live && !live.agent.canStartRun()) {
  // reattach instead of silently replacing a running session
  return await this.liveSessionStartResult(live);
}
```