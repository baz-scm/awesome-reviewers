---
title: Durable orchestration state
description: Multi-step orchestration (create-then-mutate sequences, run lifecycles,
  callback/signal routing) must be owned by the durable backend, not by ephemeral
  client-side memory, and must tolerate disconnects without duplicating side effects
  or orphaning work.
repository: cline/cline#1
label: Temporal
language: TypeScript
comments_count: 3
repository_stars: 71024
---

Multi-step orchestration (create-then-mutate sequences, run lifecycles, callback/signal routing) must be owned by the durable backend, not by ephemeral client-side memory, and must tolerate disconnects without duplicating side effects or orphaning work.

Concretely:
- Do not keep orchestration state (e.g. "push branch then create task then send message") in per-client structures like WeakMaps on a sidecar/desktop process. If the client disappears between steps, you get orphaned resources (a pushed branch with no task) and retries create duplicates (another branch, another attempt id). Move the sequence into the durable component (hub/server) so it completes atomically from the client's perspective and survives a viewer disconnecting and reconnecting.
- Treat "start" requests as idempotent with respect to in-flight work: if a session/run is already mid-execution, reattach to the live run instead of creating a new one. Starting a duplicate leaves the original run unreachable (no abort path, no queue) and causes later writes to target a stale snapshot.
  ```ts
  const live = this.sessions.get(sessionId);
  if (live && !live.agent.canStartRun()) {
    // reattach instead of replacing
    return await this.liveSessionStartResult(live);
  }
  ```
- For callbacks/signals tied to a specific connection (approvals, questions, tool results), track all registered consumers for a task, not just the originator. If the owning connection drops, route the request to another live consumer that registered the same callback, so the orchestration keeps progressing instead of failing immediately.
- When maintaining folded/derived state from a durable event log, resubscribe to the relevant change events, process one update at a time (folding any events that arrive mid-refresh), and explicitly clear fields for entries that are no longer present in an authoritative refresh — don't let stale derived state linger after the source of truth changes.

Document any remaining gaps explicitly (e.g. "this does not cover recovery from a hub crash or machine restart") so reviewers and future readers know the boundaries of the guarantee.