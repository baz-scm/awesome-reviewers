---
title: Idempotent Recovery Boundaries
description: 'When implementing error recovery/retry, treat it as a state machine
  with explicit side-effect boundaries: you must know whether the underlying action
  was dispatched/executed before offering replay, and you must keep state/diagnostics
  consistent with the actual outcome.'
repository: cline/cline#v25
label: Error Handling
language: TypeScript
comments_count: 10
repository_stars: 70891
---

When implementing error recovery/retry, treat it as a state machine with explicit side-effect boundaries: you must know whether the underlying action was dispatched/executed before offering replay, and you must keep state/diagnostics consistent with the actual outcome.

**Coding standard**
1) **Separate “request failed before dispatch” vs “after dispatch”**
- Recovery UI/actions should only offer resend/replay when you have a confirmed pre-dispatch failure.
- If you can’t confirm dispatch, plumb a dispatch signal from the transport/controller (return value or explicit event) and reconstruct a typed “sent vs unsent” error.

2) **Make retries idempotent and bounded**
- Recover exactly once for “session lost” style errors (e.g., MCP 404 session-not-found) and never replay if the retry may repeat completed side effects.
- Persistence retries must keep the failed batch and requeue it; don’t drop work on store errors.

3) **Preserve attribution and don’t over-broaden retryability**
- Avoid “timeouts are always retryable” unless you’ve proven the provider cannot have processed the request.
- Preserve timeout/abort reasons so final errors and telemetry reflect the real cause.

4) **Keep UI/runtime invariants stable during recovery**
- Don’t flip long-lived status flags (e.g., `running` → `error`) as a side effect of transient “answer failed” recovery; use transient error states/banners that don’t mutate the session’s run-state or transcript incorrectly.

5) **Never leak async failures**
- Ensure both (a) exceptions thrown inside callbacks and (b) async stream errors are captured and routed (no unhandled rejections/uncaught exceptions).

**Illustrative pattern (dispatch boundary → safe replay)**
```ts
type DispatchState =
  | { dispatched: false; error: Error; unsentPayload: unknown }
  | { dispatched: true; error: Error };

function classifySendFailure(err: unknown): DispatchState {
  // Parse typed transport error that contains a dispatch boundary.
  // If dispatched=false, it's safe to present a resend draft.
  // If dispatched=true, never offer resend (may duplicate side effects).
  // ...
  throw new Error('not implemented');
}

async function sendWithSafeReplay(payload: unknown) {
  try {
    await hub.send(payload); // transport must expose dispatch boundary
  } catch (err) {
    const state = classifySendFailure(err);
    if (!state.dispatched) {
      ui.offerResend(state.unsentPayload);
      return;
    }
    ui.showFailure(state.error); // no resend/replay
  }
}
```

**Outcome**: retries/recovery stop duplicating work, prevent wedging, preserve correct user-facing state, and ensure failures are diagnosable without introducing new unhandled async errors.