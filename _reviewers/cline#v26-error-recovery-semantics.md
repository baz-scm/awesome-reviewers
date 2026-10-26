---
title: Error recovery Semantics
description: 'When handling errors, preserve the system’s semantics: (1) classify
  failures precisely so you choose the correct recovery/retry path, (2) make recovery
  idempotent so UI/clients don’t duplicate side effects, and (3) ensure async control-flow
  never turns failures into unhandled rejections or silent degradation.'
repository: cline/cline#v26
label: Error Handling
language: TypeScript
comments_count: 9
repository_stars: 70893
---

When handling errors, preserve the system’s semantics: (1) classify failures precisely so you choose the correct recovery/retry path, (2) make recovery idempotent so UI/clients don’t duplicate side effects, and (3) ensure async control-flow never turns failures into unhandled rejections or silent degradation.

Actionable standards:
- **Define boundaries for side effects**: record whether an operation was *dispatched/accepted* vs merely *attempted* before you present resend/retry UI. Recovery should only replay when the prior outcome is truly unknown.
- **Classify retryability with tests that don’t depend on message text** (e.g., capacity codes, transport-specific “session lost”, timeout phases). Preserve existing budgets/limits; don’t blanket-enable retries for broad categories.
- **Recover exactly once when the protocol requires it**: e.g., MCP “session lost” should trigger re-handshake + single replay; canceled calls should not replay.
- **Make async flows exception-safe**: catch exceptions thrown inside `.then(...)` callbacks, and don’t launch background promises without attaching error handling. Ensure timers/observers are canceled on early failure to avoid false states.
- **Never let auxiliary systems interrupt core work**: telemetry/storage failures should be guarded and must not abort inference or core operations.
- **Fail in a way that’s observable**: distinguish “missing” from “unreadable/corrupt” config; don’t silently keep protection disabled.

Example pattern (dispatch boundary + safe async):
```ts
let dispatched = false;
try {
  const result = await hub.send(payload, {
    onDispatch: () => { dispatched = true; }
  });
  // If result indicates post-dispatch failure, present only an “unconfirmed” action.
  if (!result.ok && result.dispatched === true) {
    // Recovery must NOT cause double-send.
    return { kind: 'unconfirmed', draft: result.unsentPrompt };
  }
} catch (e) {
  // Attempt-only failure => safe resend.
  return { kind: dispatched ? 'unqueued' : 'resend', error: e };
}
```

Adopt these rules in code review by asking: *What exactly failed? Was anything already accepted/dispatched? What will recovery/retry do (once? twice?)? Are all async errors handled and surfaced without breaking unrelated logic?*