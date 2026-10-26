---
title: Error Handling Guardrails
description: 'Standard: For every failure path, (1) classify *what definitely happened*,
  (2) keep *error attribution* intact, and (3) ensure *async cleanup and UI/state
  updates* are consistent—so recovery never causes duplicate actions or corrupted
  session behavior.'
repository: cline/cline#v28
label: Error Handling
language: TypeScript
comments_count: 8
repository_stars: 70892
---

Standard: For every failure path, (1) classify *what definitely happened*, (2) keep *error attribution* intact, and (3) ensure *async cleanup and UI/state updates* are consistent—so recovery never causes duplicate actions or corrupted session behavior.

Practical rules
1) Stage-and-gate unsafe recovery
- Attach a “dispatch boundary” or equivalent signal so you can distinguish pre-action vs post-action failures.
- Only offer retries/resends when the original action is confirmed *not* to have been dispatched/processed.
- Gate whole-turn retries with existing safety conditions (stream phase, retry budget, provider retryability); do not blanket-classify timeouts as retryable.

```ts
// Pattern: only surface a resend option when failure is confirmed pre-dispatch.
if (sendFailure.dispatched) {
  // Transport may have processed the request; do not offer a resend.
} else {
  // Safe to show the unsent draft / allow replay.
}
```

2) Preserve structured error attribution
- If the system already captured a structured timeout (or other rich error), don’t lose it when abort/stream parts serialize into a string.
- When an error is classified (retryable/non-retryable, timeout phase, etc.), store the structured fields and reuse them consistently across abort/retry logic.

3) Don’t let async errors escape or “lie” to the UI
- Never convert “handled try/catch” into detached promises unless you also attach a failure handler.
- Route errors from sandbox attach/kill/cleanup through the same failure mechanism; avoid letting thrown exceptions become unhandled rejections.

```ts
// Pattern: avoid unhandled rejections from attach and from kill() paths.
void load()
  .then(attach)
  .catch((e) => handle.fail(e instanceof Error ? e : new Error(String(e))));

try {
  native.kill();
} catch (e) {
  handle.fail(e instanceof Error ? e : new Error(String(e)));
}
```

4) Make transient UI/state errors reversible
- If the runtime is still running (e.g., waiting on a pending question), transient validation failures should not permanently flip session state/transcript.
- Prefer transient/banner error states that do not append durable “error transcript” rows unless the run truly ended.

5) Cancel or avoid observation/telemetry artifacts on failure
- If you start timers/observers before an operation that can fail (spawn/start), cancel them on rejection so you don’t emit false “ran/exited” samples.

```ts
let timer: NodeJS.Timeout | undefined;
try {
  timer = setTimeout(() => report('ran'), observationMs);
  await spawn();
} catch (e) {
  if (timer) clearTimeout(timer);
  throw e;
}
```

6) Distinguish “absent” vs “unreadable” configuration
- If settings/config read fails (torn/corrupt), don’t silently keep the old default and pretend the feature is off/on.
- Either fail closed with an explicit warning or at least distinguish absent-from-unreadable so you don’t violate user expectations.

Acceptance criteria
- No recovery path can duplicate an action (resend/double-commit) because “what happened” is ambiguous.
- Timeouts and other structured failures remain correctly attributed across transport/serialization/retry.
- No unhandled promise rejections, uncancelled timers, or irreversible UI/state transitions caused solely by transient failures.