---
title: Durable orchestration state
description: Long-running, multi-step workflows (task creation, session runs, callback-driven
  interactions) must keep their orchestration and completion state in a durable, central
  component rather than in a client's in-memory/process state. Client processes (desktop
  apps, viewers, sockets) can disconnect, crash, or restart at any point, and the
  workflow must not assume...
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Temporal
language: TypeScript
comments_count: 3
repository_stars: 70964
---

Long-running, multi-step workflows (task creation, session runs, callback-driven interactions) must keep their orchestration and completion state in a durable, central component rather than in a client's in-memory/process state. Client processes (desktop apps, viewers, sockets) can disconnect, crash, or restart at any point, and the workflow must not assume they stay alive.

Apply these rules:
1. Anchor multi-step sequences (e.g., "push branch" then "create task") in the durable side (hub/core), not in ephemeral client-side maps (`WeakMap`, in-memory caches). If a client disappears between steps, the sequence must either be resumable or abort atomically — never leave orphaned partial state (e.g., a pushed branch with no corresponding task) that causes duplicate work on retry.
2. Don't pin callbacks/signals for an in-flight run to a single originating client. Track all clients/apps that have registered interest in a run's callbacks, and route requests to any other currently-connected one if the original disconnects, so the run can keep progressing instead of stalling.
3. Scope completion/timeout tracking (recovery deadlines, retry counters) per run/attempt, not globally or per-connection. Only clear a deadline via an authoritative, correlated terminal signal for that specific run (matching reply, terminal event, or heartbeat) — never from unrelated events like a generic reconnect. If no such signal arrives within the bound, fail fast with a clear timeout rather than hanging indefinitely.

Example pattern for reattaching instead of silently replacing a live run:

```ts
const live = this.sessions.get(sessionId);
if (live && !live.agent.canStartRun()) {
  if (input.prompt?.trim()) {
    throw new Error(
      `Session ${sessionId} already has a run in progress; queue the prompt instead.`,
    );
  }
  return await this.liveSessionStartResult(live);
}
```

This keeps orchestration correct and recoverable across client disconnects, crashes, and reconnects, and prevents duplicated side effects, stuck runs, or indefinite hangs.</description>
</invoke>
