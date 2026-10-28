---
title: Durable, idempotent orchestration
description: Multi-step, side-effecting workflows (e.g. push-then-create, start-then-run)
  must not depend on a single ephemeral connection or in-memory map for their progress.
  If a client/viewer disconnects or a process restarts mid-sequence, the orchestration
  must either continue in a durable component (a server/hub that outlives the connection)
  or be safely resumable,...
repository: "cline/cline\t"
label: Temporal
language: TypeScript
comments_count: 3
repository_stars: 70947
---

Multi-step, side-effecting workflows (e.g. push-then-create, start-then-run) must not depend on a single ephemeral connection or in-memory map for their progress. If a client/viewer disconnects or a process restarts mid-sequence, the orchestration must either continue in a durable component (a server/hub that outlives the connection) or be safely resumable, never silently abandoned or blindly re-run from scratch.

Concretely:
- Keep orchestration state that spans multiple side-effecting steps in a durable owner (server/hub), not in transient client-side state (e.g. a `WeakMap` keyed to a connection). A sequence like "push branch" → "create task" must be executed by the durable side so a viewer disconnecting between steps can't leave an orphaned branch or trigger a duplicate push on retry.
- Before starting new work, check whether equivalent work is already in flight and reattach/resume instead of creating a duplicate or orphaning the original:
```ts
const live = this.sessions.get(sessionId);
if (live && !live.agent.canStartRun()) {
  // Don't replace an in-progress run: it becomes unreachable (no abort,
  // no queue) and writes resolve against a stale snapshot.
  return await this.liveSessionStartResult(live);
}
```
- When the party responsible for a step (e.g. answering callbacks, owning a session) disconnects, fail over to another connected party that can take over the same role, rather than failing the whole workflow outright.
- When state is derived from a stream of events, ensure recovery handles missed or out-of-order events by resubscribing/resyncing on relevant change signals and reconciling stale entries, instead of assuming every event is seen exactly once.

Document these guarantees and their limits explicitly (e.g. "survives viewer disconnect, but not a hub crash or machine restart") so downstream consumers know what failure modes are actually covered, and add tests that simulate the disconnect/restart/failover scenario, not just the happy path.