---
title: Telemetry correctness standards
description: 'Observability instrumentation must produce accurate, contract-compliant,
  and side-effect-free data.


  Apply these rules:

  1) Use typed/categorized telemetry APIs'
repository: cline/cline#v27
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70892
---

Observability instrumentation must produce accurate, contract-compliant, and side-effect-free data.

Apply these rules:
1) Use typed/categorized telemetry APIs
- Prefer cataloged event constants + typed capture helpers over raw event strings.
- Keep event/property shapes consistent and avoid sending unsanitized/raw or hashed prompt data.

2) Respect opt-out and existing plumbing
- Route events through the shared emit/capture path so opt-out and renaming are applied consistently.

3) Make lifecycle timing explicit (especially for tracing)
- Ensure error/exception details are recorded before the relevant span/generation lifecycle closes.
- For “started” telemetry, always emit a matching terminal outcome (succeeded/failed/aborted) and don’t attribute stale causes across turns.

4) Prevent misleading metrics
- Emit failure reasons only when they truly apply (e.g., distinguish TIMEOUT vs NO_OUTPUT/ask failures).
- Cancel/clear sampling windows and timers on early failures/spawn errors to avoid false samples.

5) Keep instrumentation side-effect-free
- Don’t mutate runtime/session configuration in ways that change core semantics (e.g., sessionId, restart detection). Attach telemetry via hooks/context, not by rewriting bootstrap inputs.

6) Lock correctness with tests
- Add regression tests that assert emitted event names/properties and (when applicable) trace span status/exception presence.

Example pattern (lifecycle-safe error capture):
```ts
function onStepStart(){ streamRetryBackoff?.startStep(); }

async function onError({ error }) {
  const wait = streamRetryBackoff?.onError(error);
  if (!wait) return;

  // Record error + retry notice immediately; don’t wait for a later stream/end hook
  streamTelemetry.captureError(error);
  context.telemetry?.capture({
    event: CORE_TELEMETRY_EVENTS.SOME_RETRY,
    properties: { attempt: wait.attempt, delayMs: wait.delayMs },
  });

  request.emitStatusNotice?.(`retrying in ${wait.delayMs}ms`);
}
```
Follow up with tests asserting the correct terminal outcome and event properties under: recovered success, recovered failure, and time/lifecycle edge cases.