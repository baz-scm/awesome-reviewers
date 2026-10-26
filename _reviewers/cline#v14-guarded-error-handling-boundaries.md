---
title: Guarded Error Handling Boundaries
description: 'Standard: every error path must be explicitly classified, handled within
  the owning async boundary, and must not silently change invariants (retryability,
  user/session state, or side effects).'
repository: cline/cline#v14
label: Error Handling
language: TypeScript
comments_count: 11
repository_stars: 70876
---

Standard: every error path must be explicitly classified, handled within the owning async boundary, and must not silently change invariants (retryability, user/session state, or side effects).

Practical rules:
1) **No “rare-state fallthrough”**: if a required artifact/state is missing, prefer throwing (or returning a failure result) over continuing into logic that can replace/duplicate work.
2) **Classify errors before retry/recovery**: retries/replays must be gated by error type and real transport semantics (timeouts, session-lost, stream vs request retry). Never blanket-mark timeouts as retryable, and never recover with the wrong error matcher.
3) **No unhandled promise rejections**: every `then(...)` chain that can throw during attachment/cleanup must be followed by a catch that routes the error to the same controlled failure mechanism.
4) **Never detach a failing promise without a handler**: if you intentionally don’t await, you still must attach a `.catch()` (or otherwise ensure the failure is logged/recorded and doesn’t leave misleading UI state).
5) **Preserve invariants during transient failures**: retryable UI/agent failures should not flip the session into a terminal error state or corrupt transcript/attribution. Decide “transient vs terminal” and enforce it consistently.
6) **Don’t cancel timers/observers incorrectly**: if execution fails early (e.g., spawn fails), cancel any later “observation” timers so you don’t emit false runtime samples.

Code pattern (avoid missed async exceptions/unhandled rejections):
```ts
// BAD: attach throws -> unhandled rejection; handle never receives failure
void loadMxc().then((mxc) => {
  return handle.attach(mxc.spawn(req));
});

// GOOD: attach+spawn exceptions funnel into one controlled failure path
loadMxc()
  .then((mxc) => mxc.spawn(req).then((p) => handle.attach(p)))
  .catch((err: unknown) => {
    const reason = err instanceof Error ? err.message : String(err);
    handle.fail(new Error(`Sandbox failed: ${reason}`));
  });

// BAD: intentionally detached promise without catch
checkpointTracker.commit().then((h) => update(h));

// GOOD: detached work still reports failures safely
checkpointTracker.commit()
  .then((h) => update(h))
  .catch((e) => {
    // log/telemetry; keep original error semantics
    Logger.error('Checkpoint commit failed', e);
  });
```

Checklist for PRs in this area:
- What error class is this (retryable/terminal, transient/persistent)?
- What guarantees prevent duplication (side effects) on retry?
- Are all promise chains/timers/listeners either awaited or caught within the same boundary?
- Does the fix preserve user/session state invariants (status/transcript/ownership) across retries?
- Are you failing loudly (throw/explicit failure) when the safe fallback would corrupt invariants?