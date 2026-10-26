---
title: Telemetry Fidelity Standards
description: 'When adding/changing instrumentation, treat telemetry like an API contract:
  it must be safe, correctly attributed, and lifecycle-consistent.


  **Apply this checklist**'
repository: cline/cline#v7
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70865
---

When adding/changing instrumentation, treat telemetry like an API contract: it must be safe, correctly attributed, and lifecycle-consistent.

**Apply this checklist**
1. **Emit the right cause, in the right scope**
   - Ensure failure/reason fields are cleared/reset at the correct boundary (e.g., per turn, not per run) to avoid stale attribution.
   - Don’t broaden catch blocks into incorrect reason enums; add a distinct reason for the actual condition.
   - Preserve provider details only when that provider failure is truly the run-ending failure.

2. **Make tracing/telemetry lifecycle consistent**
   - If you record `phase: started`, you must always record a terminal phase (`succeeded`/`failed`) along every path.
   - Ensure the error is recorded **before** the relevant spans/steps close; late `onEnd`/post-close hooks can leave generation spans unmarked.

3. **Avoid metric inflation and duplication**
   - Don’t double-count: if there is a central pipeline (runtime→adapter→handler), instrument once and rely on the canonical event.
   - Track progress only for the runtime events that actually represent progress; streaming chunk assembly alone may not be observable progress.

4. **Governance + safety**
   - Use typed helpers/catalog constants where required by scope; avoid raw event-name strings.
   - Sanitize/redact: never emit prompt text, hashes, or other sensitive fields; respect opt-out.
   - Telemetry capture should never throw; failing providers/hooks must not break core behavior.

**Example patterns**
- *Phase closure (terminal-before-rethrow)*
```ts
captureTaskLifecycle(EVENT, { phase: "started" });
try {
  // ... emit notices, perform work ...
} catch (err) {
  captureTaskLifecycle(EVENT, {
    phase: "failed",
    eventType: isAbort(err) ? "aborted" : "retry_threw",
  });
  throw err;
}
captureTaskLifecycle(EVENT, { phase: "succeeded" });
```

- *Reset attribution per turn* 
```ts
// Clear before generating a new assistant turn, so failures never inherit
// the previous turn's finish reason.
this.state.lastFinishReason = undefined;
```

- *Reason correctness / classification* 
```ts
if (!output.trim()) {
  telemetry.captureTerminalOutputFailure("NO_OUTPUT");
}
```

- *Never mutate session/telemetry truth during wiring*
```ts
// Telemetry wiring should attach hooks only; do not rewrite sessionId semantics
// in a way that changes core's restart/read-only logic.
return { ...originalConfig, hooks };
```

Use this standard to prevent observability regressions like misclassified metrics, stale failure causes, missing generation-level errors, duplicated usage counters, and inconsistent tracing lifecycles.