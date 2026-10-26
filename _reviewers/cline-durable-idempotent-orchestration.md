---
title: Durable, idempotent orchestration
description: Multi-step orchestrated operations (git push + task creation, remote
  command execution, etc.) must tolerate process restarts, disconnects, and retries
  without producing duplicate side effects or hanging indefinitely. Avoid storing
  critical orchestration state only in ephemeral, process-local structures (e.g.,
  in-memory WeakMaps in a sidecar); if a step can...
repository: cline/cline
label: Temporal
language: TypeScript
comments_count: 2
repository_stars: 70886
---

Multi-step orchestrated operations (git push + task creation, remote command execution, etc.) must tolerate process restarts, disconnects, and retries without producing duplicate side effects or hanging indefinitely. Avoid storing critical orchestration state only in ephemeral, process-local structures (e.g., in-memory WeakMaps in a sidecar); if a step can run outside the lifetime of the originating process, model it as a durable, resumable workflow (e.g., in core/Hub) so progress survives disconnects. When retrying a partially-completed sequence, use a stable idempotency/attempt key so a retry resumes or reconciles the existing side effect (e.g., branch, task) instead of creating a new one.

Similarly, any timeout or recovery deadline tied to an in-flight unit of work should be scoped to that specific unit (not a shared/global timer) and must only be cleared by a definitive, correlated completion signal for that unit — a matching reply, terminal event, or heartbeat. Successful reconnection or unrelated state changes should not implicitly clear deadlines. If no such signal arrives before the deadline, fail fast with a clear error rather than leaving the caller waiting indefinitely.

Example pattern:
```ts
// Per-run deadline, keyed by attempt id, cleared only by that run's own signal
runDeadlines.set(attemptId, setTimeout(() => rejectRun(attemptId, "no completion signal"), RECOVERY_TIMEOUT_MS));

function onRunEvent(attemptId: string, evt: TerminalEvent | Heartbeat | CorrelatedReply) {
  clearTimeout(runDeadlines.get(attemptId));
  runDeadlines.delete(attemptId);
}
```
This ensures retries are safe (no duplicate branches/tasks) and that callers get deterministic, bounded outcomes even across reconnects or crashes.</description>
</invoke>
