---
title: Bounded Recovery And Safe Async
description: 'When handling errors, recovery, and retries: (1) classify failures precisely,
  (2) keep recovery bounded and conditional to avoid duplicate side effects, and (3)
  ensure every async failure path is handled (no unhandled rejections/uncaught stream
  errors), with best-effort degradation that preserves critical outputs/diagnostics.'
repository: cline/cline#v18
label: Error Handling
language: TypeScript
comments_count: 15
repository_stars: 70884
---

When handling errors, recovery, and retries: (1) classify failures precisely, (2) keep recovery bounded and conditional to avoid duplicate side effects, and (3) ensure every async failure path is handled (no unhandled rejections/uncaught stream errors), with best-effort degradation that preserves critical outputs/diagnostics.

Practical rules:
1) No silent fallthrough after “rare” invariants break
- If a guard exists because continuing would orphan/duplicate/replace live state, fail fast instead of letting control flow proceed.

2) Make retries conditional and side-effect aware
- Don’t blanket-retry on timeouts; a timeout often means “client stopped waiting,” not “provider is transient.”
- Separate “provider retry within the adapter” from “whole-turn retry.” Preserve the existing bounded retry policy rather than bypassing it.

3) Preserve the boundary that defines “was it dispatched?”
- For orchestration (handoff, hub sends, multi-step workflows), record the dispatch/confirmation boundary. Misclassifying it leads to “resend” paths that can duplicate prompts/commands.

4) Always route async exceptions into the same error channel
- Catch exceptions thrown inside callbacks (e.g., in `.then(attach)`), and handle stream errors (stdin/EPIPE) with listeners so they can’t crash the host.
- Never leave detached promises unobserved when failures should be logged/recorded.

5) Bound every network/long operation with abort + consistent parsing
- Ensure fallback paths also use AbortSignal/timeouts; also guard option parsing so missing/malformed config doesn’t silently disable features.

6) Degrade safely: telemetry/storage should not break inference or lose important results
- If persistence/telemetry fails, log/warn and preserve at least the preview/partial data so you don’t turn degradation into data loss or incorrect user state.

Code patterns:
- Ensure async “attach” exceptions are captured:
```ts
export function spawnInProjectSandbox(...): ChildProcess {
  const handle = new SandboxedProcess();
  void loadMxc()
    .then((mxc) => mxc.spawn(/*...*/).then((p) => handle.attach(p)))
    .catch((err) => {
      handle.fail(new Error(String(err)));
    });
  return handle as unknown as ChildProcess;
}
```
- Avoid whole-turn retries for timeouts; treat timeout as a non-evidence of transience:
```ts
function retryable(error: unknown): boolean {
  if (isTimeoutReason(error)) return false; // or only retry within bounded adapter policy
  return isRetryableBeyondSdkRetries(error);
}
```
- Don’t leave detached operations unhandled:
```ts
try {
  await say("checkpoint_created");
  this.checkpointTracker.commit().then(async (hash) => {
    await this.messageStateHandler.updateClineMessage(/*...*/);
  }).catch((e) => {
    console.error("checkpoint commit failed", e);
  });
} catch (e) {
  // normal handling
}
```

Adopting this standard prevents orphaned live state, duplicated side effects from misclassified retries/resends, host crashes from stream/unhandled promise errors, and “looks healthy but isn’t” degraded behavior in user-facing features.