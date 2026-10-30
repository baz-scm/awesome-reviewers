---
title: Re-validate state after awaits
description: 'The overwhelming majority of concurrency bugs found in review were time-of-check-to-time-of-use
  races: code checked a condition (session is current, resource is unused, generation
  matches, lock is free) and then, after an `await` yielded control, acted as if that
  condition still held. Another concurrent caller, teardown, reconnect, or retry had
  changed the...'
repository: cline/cline#"><b>zze3729958
label: Concurrency
language: TypeScript
comments_count: 32
repository_stars: 71067
---

The overwhelming majority of concurrency bugs found in review were time-of-check-to-time-of-use races: code checked a condition (session is current, resource is unused, generation matches, lock is free) and then, after an `await` yielded control, acted as if that condition still held. Another concurrent caller, teardown, reconnect, or retry had changed the world in between, so the resumed continuation clobbered newer state, replayed a stale result, double-ran a side effect, or leaked a resource.

To prevent this class of bug:
1. **Re-check right before acting, not just before awaiting.** Every `await` is a point where shared mutable state can change; re-validate immediately after each one, not only once at the top of the function. If several awaits happen in sequence, re-check after every one of them before producing a visible side effect (a write, an emit, a dispose).
2. **Use generation/epoch counters or identity tokens to detect staleness.** Stamp a monotonically increasing counter (or capture the live object reference) before starting async work; compare it after resuming to tell a superseded attempt from the current one, instead of relying on booleans that can't distinguish "still mine" from "replaced by something equivalent."
3. **Claim or reserve a resource synchronously before yielding.** When a resource must not be grabbed twice (a pending-answer promise, a session slot, a cache key, a file), claim/lock it in the same synchronous tick as the check, before any `await`, so a second concurrent caller cannot interleave between check and claim.
4. **Serialize operations on the same shared resource instead of letting them race.** Prefer a per-key queue/lock (chaining onto the in-flight promise) over ad hoc flags, so overlapping calls apply in a defined order and the last writer predictably wins (or merges), rather than whichever happens to resolve last by accident.
5. **Keep side effects atomic with the check that guards them.** Where possible, replace "check flag → await → act on stale flag" with "set the terminal state and act in the same synchronous step" so no concurrent code can observe or exploit the gap.

Example of the pattern to apply:
```ts
async function releaseRuntime(session: ActiveSession): Promise<void> {
  // A replacement session may take this slot at any await below.
  const displaced = () => sessions.get(session.sessionId) !== session;
  await refreshGitMetadata(session);
  if (displaced()) return; // re-check: another start may have won the slot
  await writeStatus(session, "cancelled");
  if (displaced()) return; // re-check again before the next side effect
  await emitEndedEvent(session);
}
```
Apply this standard whenever introducing an `await` inside code that reads-then-writes shared state (session/connection registries, caches, files, in-memory maps, pending-request maps): identify every mutation that follows an await and ask "could this value have changed while I was suspended, and if so, is my guard checked close enough to the point of use?"</description>
</invoke>
