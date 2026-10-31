---
title: Decouple orchestration from client lifetime
description: Multi-step workflows and their state must not be owned by a transient
  client/viewer connection. If a client disconnects mid-sequence (e.g., between pushing
  a branch and creating the task, or mid-run of a session), orphaned side effects,
  duplicate retries, or unreachable sessions with stale snapshots can result. Move
  ownership of critical state transitions...
repository: cline/cline?foo=bar
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 71082
---

Multi-step workflows and their state must not be owned by a transient client/viewer connection. If a client disconnects mid-sequence (e.g., between pushing a branch and creating the task, or mid-run of a session), orphaned side effects, duplicate retries, or unreachable sessions with stale snapshots can result. Move ownership of critical state transitions and side effects (git push + create, session run state, callback routing) into a durable component (hub/core) that survives individual client disconnects, and make the sequence resilient to disconnection at any point rather than relying on the client staying connected to finish it.

For in-flight work, never silently replace it on reconnect/restart — reattach instead, and fail over responsibilities (e.g., callback handling) to another connected client if the original owner disappears:

```ts
const live = this.sessions.get(sessionId);
if (live && !live.agent.canStartRun()) {
  if (input.prompt?.trim()) {
    throw new Error(`Session ${sessionId} already has a run in progress; queue the prompt instead.`);
  }
  return await this.liveSessionStartResult(live); // reattach, don't replace
}
```

When no connected party can take over (e.g., no client registered the needed callback), fail fast with a clear, actionable error rather than hanging or silently corrupting state. Document the remaining gaps explicitly (e.g., "does not guarantee recovery from a hub crash or machine restart") so callers know the actual fault-tolerance boundary.