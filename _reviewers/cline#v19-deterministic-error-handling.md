---
title: Deterministic Error Handling
description: 'Adopt a single rule-set for failures: **classify the error, bound the
  recovery, and make state transitions deterministic**. This prevents orphaned work,
  misleading UI/status, and unhandled promise/stream failures.'
repository: cline/cline#v19
label: Error Handling
language: TypeScript
comments_count: 12
repository_stars: 70885
---

Adopt a single rule-set for failures: **classify the error, bound the recovery, and make state transitions deterministic**. This prevents orphaned work, misleading UI/status, and unhandled promise/stream failures.

Practical standards:
1) **No fallthrough after invariant failures**: if a “should not happen” path still produces an invalid state (e.g., missing artifacts after ensuring persistence), either **throw** or explicitly prove the invariant before proceeding—never let the code reach a branch that can replace live state.
2) **Bound ownership-less waits**: when a request can outlive its owner (owner gone/unregistered) and nothing will answer it, add **deadlines** and cleanup so the system can’t wait forever.
3) **Retryability must be semantics-based**: do not treat all timeouts as transient. Preserve provider/transport semantics (SDK abort/timeout attribution, finishReason mapping) and add tests that cover both “retry allowed” and “retry unsafe” cases.
4) **Cleanup must be in `finally` and state-safe**: when replacing/releasing session/runtime resources, release old state in `finally`, but guard against deleting the replacement (compare references/identity).
5) **No unhandled async failures**: always catch promise rejections created from “fire-and-forget” `.then(...)`, and attach handlers for stream write failures (stdin/stdout) to avoid host-level uncaught exceptions.
6) **Stream/transport errors are still “real errors”**: EPIPE/early stream closure should be absorbed, annotated, and routed into the same failure channel as exit/rejection.

Example (pattern):
```ts
async function safeReplaceSession(live: Session | undefined, input: StartInput) {
  if (live && !live.agent.canStartRun()) {
    // If persistence fails to produce required invariants, stop.
    await ensureSessionPersisted(live);
    const artifacts = live.artifacts;
    if (!artifacts) {
      throw new Error(`Invariant broken: session persisted but artifacts missing for ${input.config.sessionId}`);
    }
    return; // enqueue behind the live turn instead of replacing
  }

  // Replacement path: always clean up old state, but never tear down the new resident.
  const oldResident = live;
  try {
    await startNewSession(input);
  } finally {
    if (oldResident && /* identity still matches */ wasNotReplacedByNew(oldResident)) {
      await releaseSessionRuntime(oldResident, "session_replaced");
    }
  }
}
```

If you apply these consistently, the team will stop seeing: indefinite hangs, orphaned work, stranded state, misleading success UI, and host crashes from unhandled async/stream errors—all core outcomes of the Error Handling category.