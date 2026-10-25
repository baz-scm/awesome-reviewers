---
title: Robust async error handling
description: 'Standard: when adding error recovery, retries, or asynchronous work,
  preserve invariants by (1) wiring every failure into the owning state machine, (2)
  keeping retry/timeout attribution explicit and conservative, and (3) ensuring UI/state
  changes made on error remain repairable.'
repository: ClInE/cLiNe
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 70838
---

Standard: when adding error recovery, retries, or asynchronous work, preserve invariants by (1) wiring every failure into the owning state machine, (2) keeping retry/timeout attribution explicit and conservative, and (3) ensuring UI/state changes made on error remain repairable.

Apply:
1) Enforce post-condition invariants (no fallthrough)
- If a step is required to prevent a known bad state (e.g., “persist session so artifacts must exist”), then missing required data is a logic error: throw immediately instead of falling through to replacement logic.

```ts
await ensureSessionPersisted(liveSession);
if (!liveSession.artifacts) {
  // Invariant broken: continuing can orphan a running agent.
  throw new Error(`Session ${requestedSessionId} persisted without artifacts`);
}
```

2) Never leave detached Promises or exception paths unhandled
- Either `await` the async operation inside the try/catch that owns the error semantics, or attach a `.catch()` that routes into your failure handler.

```ts
// Bad: unhandled rejection can break chat state/UI.
checkpointTracker.commit().then(async () => say('checkpoint_created'));

// Good: keep failure in the same control flow.
try {
  await say('checkpoint_created');
  const commitHash = await checkpointTracker.commit();
  await updateCheckpoint(commitHash);
} catch (err) {
  logAndHandleCheckpointFailure(err); // same intent as previous behavior
}
```

- For async “then(attach)” patterns, ensure exceptions thrown inside `attach()` are also caught (use `.then(fn).catch(fn)` rather than only `.then(fn, onError)`).

3) Retry/timeout classification must be explicit
- Do not grant additional “whole-turn” retry budget for timeouts unless your existing retryability rules explicitly allow it.
- Preserve timeout attribution across stream/abort boundaries so the final error message/result reflects the true cause.

4) Don’t flip terminal UI/session state for errors that the runtime can’t repair
- If the sidecar/session is still blocked and the error cannot be corrected by subsequent runtime recovery, avoid changing durable status/transcript rows to a state that will linger.
- Prefer transient/banner-style error states that don’t corrupt persisted history.

5) Telemetry and logging must not interrupt core execution
- Treat telemetry emission as non-blocking: never allow telemetry exceptions to abort inference, tool execution, or orchestration.

6) Preserve completed side effects across retries/stream failures
- If a retry boundary occurs after local tool activity already succeeded, ensure history records include those completed results; don’t discard side effects purely because the later stream failed.

Quick checklist for PRs in this category
- [ ] Every async branch is awaited or has an owner-level catch.
- [ ] No fallthrough after required-precondition/persistence steps.
- [ ] Retry eligibility is derived from explicit error classification (timeouts ≠ always retryable).
- [ ] User-visible status/transcripts changed on error are repairable (or use transient error patterns).
- [ ] Telemetry cannot throw into inference/orchestration.
- [ ] Retries don’t drop already-completed tool side effects/results.