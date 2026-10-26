---
title: Error Semantics and Recovery
description: 'When handling failures, treat “error meaning” as part of the contract:
  never silently convert unrelated failures into valid outputs, never leave async
  error paths unobserved, and never let recovery/telemetry/state machines corrupt
  invariants.'
repository: cline/cline#x
label: Error Handling
language: TypeScript
comments_count: 10
repository_stars: 70861
---

When handling failures, treat “error meaning” as part of the contract: never silently convert unrelated failures into valid outputs, never leave async error paths unobserved, and never let recovery/telemetry/state machines corrupt invariants.

Apply these rules:

1) Don’t fall through when invariants break
- If a guard step is meant to prevent an orphan/duplicate/live-replacement situation, and an impossible/rare state is still reachable, stop immediately.
- Pattern: after an `ensureX()` that “should” guarantee a property, validate and `throw` if it’s still missing.

2) Classify failures precisely (no fake success)
- Only map a failure into a “missing”/“not present” outcome when you can prove it’s the missing case (e.g., git reports a missing path/object). Other failures (limits, unknown errors) must propagate as real errors.

3) Async error hygiene: cover both reject and throw
- A `Promise` chain catches rejections, but synchronous exceptions *inside later continuations* may bypass earlier catches and produce unhandled rejections / hung operations.
- Prefer `try/catch` around multi-step attachment logic, or ensure `.catch()` is attached to the full chain.

Example (fixing “catch rejection but not throw inside attach”):
```ts
const handle = new SandboxedProcess();
void loadMxc()
  .then((mxc) => mxc.spawn(/* ... */))
  .then(
    (sandboxed) => {
      // If this throws, it must be caught by the same chain.
      return handle.attach(sandboxed);
    },
  )
  .catch((error) => {
    const reason = error instanceof Error ? error.message : String(error);
    handle.fail(new Error(`Couldn't keep this command inside project (${reason})`));
  });
```

4) Recovery eligibility must follow semantics (timeouts/abort/cancellation)
- Don’t broaden retryability (e.g., making all timeouts whole-turn retryable). A timeout/cancellation typically means the client stopped waiting, not that the provider failure is transient.
- Preserve attribution details: if the abort reason becomes stringified, still use the original captured timeout metadata.

5) Preserve state machine invariants during recovery
- Transient failures that the system cannot repair on the server side must not permanently degrade session state/UI transcripts.
- Recovery must preserve already-completed side effects/results (e.g., executed tool calls) and avoid repeating them when the response is unfinished.

6) Cancel derived observations on early failure
- If you start a timer/observation window to produce telemetry, cancel it when the underlying process never started (otherwise you emit false “ran and exited” samples).

7) Never leave critical background work unobserved
- If a detached promise affects persisted metadata/UX consistency (e.g., checkpoint creation), ensure failures are either awaited or caught/logged; otherwise you risk unhandled rejections and stale UI (e.g., “checkpoint_created” without a hash).