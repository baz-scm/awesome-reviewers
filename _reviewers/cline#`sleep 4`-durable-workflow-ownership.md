---
title: Durable workflow ownership
description: Multi-step orchestration that has side effects (e.g., pushing a branch,
  then creating a task) must not depend on a transient client staying connected. If
  a disconnect can occur between two dependent steps, the sequence should be owned
  and executed end-to-end by a durable backend component (e.g., a Hub/service), not
  tracked in client-local state like a...
repository: cline/cline#`sleep 4`
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 70979
---

Multi-step orchestration that has side effects (e.g., pushing a branch, then creating a task) must not depend on a transient client staying connected. If a disconnect can occur between two dependent steps, the sequence should be owned and executed end-to-end by a durable backend component (e.g., a Hub/service), not tracked in client-local state like a WeakMap in a desktop sidecar. The client should hand off the full plan (snapshot, summary, inputs) in one call so the durable side performs the push, creation, and initial send without requiring the originating viewer to remain connected; this prevents orphaned side effects and duplicate retries (e.g., a branch pushed with no task, followed by another branch on retry).

Complementary to this, any recovery/acknowledgement tracking for in-flight operations must be scoped per operation (not global), survive reconnects/re-registration, and only be cleared by definitive completion evidence: a correlated reply, a terminal event, or a heartbeat specific to that run. If no such evidence arrives, the operation must still resolve deterministically within a bounded timeout (e.g., reject after 60s) rather than hang indefinitely. Cover these cases with tests: no-replay timeout, live run continuing past the deadline, and terminal-event replay without re-sending the original request.

Example pattern:
```ts
// Bad: client owns multi-step sequence in local state
const plans = new WeakMap<SidecarContext, Map<string, HandoffPlan>>();
await applyHandoffGit(plan);       // step 1
await cloud.create(plan.summary);  // step 2 — lost if client closes here

// Good: hand off the full plan so the durable side executes all steps atomically
await hub.create({ localGit: snapshot, initialMessage: summary });
```

Document explicitly when such guarantees stop (e.g., they do not cover a full backend crash or host restart) so downstream consumers understand the failure boundary.