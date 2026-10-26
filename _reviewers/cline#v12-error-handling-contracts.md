---
title: Error-handling Contracts
description: When an operation fails, code must (a) classify the failure precisely,
  (b) route every async/stream failure into the same controlled outcome (no unhandled
  rejections/uncaught exceptions), and (c) report user-facing/telemetry messages that
  match the real outcome—never a speculative fallback.
repository: cline/cline#v12
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 70872
---

When an operation fails, code must (a) classify the failure precisely, (b) route every async/stream failure into the same controlled outcome (no unhandled rejections/uncaught exceptions), and (c) report user-facing/telemetry messages that match the real outcome—never a speculative fallback.

Apply this checklist:
1) **Failure contracts must be explicit**
- If fallback/transfer would change behavior (capability takeover, session ownership, resend), either make the takeover contract explicit or **fail clearly**.
- Include structured reasons (e.g., `disconnected | detached | cancelled_while_waiting`) for observability.

2) **Retry only when proven safe**
- Avoid blanket rules like “all timeouts are retryable”.
- Preserve existing “provider retry” semantics: if a retry budget is managed elsewhere, do not bypass it in a new layer.

3) **No stray async failures**
- Any detached promise chain must have a catch that routes into the intended failure handling.
- Stream write errors (stdin/socket) and “kill/cleanup” failures must be caught and routed (not allowed to become host unhandled rejections).

4) **Attribution must reflect the current outcome**
- Don’t base diagnostics on an arbitrary transcript “tail”; tie lifecycle/errors to the current turn/session outcome.

Example pattern (single controlled failure path + precise classification):
```ts
async function withRecovery<T>(
  action: () => Promise<T>,
  classify: (e: unknown) => 'retryable' | 'recoverable' | 'fatal',
  recover: () => Promise<void>,
  fail: (e: unknown) => Promise<T>,
): Promise<T> {
  try {
    return await action();
  } catch (e) {
    const mode = classify(e);
    if (mode === 'fatal') return await fail(e);
    if (mode === 'recoverable') {
      await recover();
      return await action();
    }
    // retryable: only if you *know* it’s safe (bounded + budgeted elsewhere)
    return await action();
  }
}
```

Concrete “don’ts” mirrored from the issues:
- Don’t remove/avoid capability ownership transfer by guessing; fail with a user message and telemetry reason.
- Don’t detach an async operation without a `.catch()` when failures should be recorded/logged.
- Don’t blanket-mark timeouts retryable; keep timeout attribution and retry semantics correct.
- Don’t ignore async cleanup/kill/stream failures—route them into the same failure handling path.
- Don’t mis-attribute lifecycle diagnostics by inspecting the wrong chunk/turn.
