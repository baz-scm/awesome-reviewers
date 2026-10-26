---
title: Deterministic Error Recovery
description: 'Aim for error handling that is (a) deterministic, (b) classification-driven,
  and (c) recovery-safe.


  Apply these rules:

  1) **No fallthrough after invariant checks**: if a helper is supposed to assign/throw,
  treat “missing after ensure” as a hard error. Don’t let rare null/undefined paths
  replace live sessions or produce misleading “success”.'
repository: cline/cline?x=1
label: Error Handling
language: TypeScript
comments_count: 17
repository_stars: 70861
---

Aim for error handling that is (a) deterministic, (b) classification-driven, and (c) recovery-safe.

Apply these rules:
1) **No fallthrough after invariant checks**: if a helper is supposed to assign/throw, treat “missing after ensure” as a hard error. Don’t let rare null/undefined paths replace live sessions or produce misleading “success”.
2) **Classify errors before retry/recovery**:
   - Only treat “not found/missing path/object” as an absent side; everything else (limits, corrupt objects, truncation caps) must surface and not be coerced into deletions.
   - Timeouts are *not* automatically proof of transient failure—preserve the existing retryability/budget logic.
3) **Make retries boundary-aware and idempotent**:
   - Track whether an operation was dispatched vs pre-dispatch; on failure, only offer “resend” when it’s safe (avoid double-send).
   - Persist orchestration checkpoints so an app restart/retry can’t re-push/branch into duplicated side effects.
4) **Never leak unhandled async errors**:
   - Wrap async attach/setup work; catch exceptions that otherwise become unhandled rejections.
   - Route kill/fail paths through a single error handling mechanism (don’t let kill() throw escape).
   - Attach stream `error` listeners (EPIPE/write failures) so the host process doesn’t crash; surface the more useful “exit” diagnostics.
   - Handle background promise rejections; never rely on “silently fails” without a `.catch()` or equivalent.
5) **Preserve correctness metadata through failure paths**: if you hit caps (e.g., truncated file reads), carry a `truncated` flag to the UI and avoid generating fake diffs.

Minimal pattern to follow:
```ts
async function safeOperation<T>({
  invariantEnsure,
  classify,
  canRecover,
  doWork,
}: {
  invariantEnsure: () => Promise<void>;
  classify: (e: unknown) => { kind: "missing" | "timeout" | "other" };
  canRecover: (kind: "missing" | "timeout" | "other") => boolean;
  doWork: () => Promise<T>;
}): Promise<T> {
  await invariantEnsure().catch((e) => {
    // Invariant failure should not be hidden.
    throw e;
  });

  try {
    return await doWork();
  } catch (e) {
    const { kind } = classify(e);
    if (!canRecover(kind)) throw e;
    // Recovery must be boundary-safe and not duplicate side effects.
    throw new Error("Recovery not implemented: ensure idempotency + dispatch boundary tracking");
  }
}
```

Outcome: developers get predictable failures, correct user-facing error messages, safe recovery/retries that don’t duplicate side effects, and no host-crashing unhandled async errors.