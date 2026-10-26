---
title: Telemetry Correctness Standard
description: 'All observability instrumentation must preserve telemetry contracts
  *and* report correct, non-misleading outcomes.


  Apply these rules:


  1) Use approved event identifiers & helpers (within the correct scope)'
repository: cline/cline#v12
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70872
---

All observability instrumentation must preserve telemetry contracts *and* report correct, non-misleading outcomes.

Apply these rules:

1) Use approved event identifiers & helpers (within the correct scope)
- In core/first-party areas, emit only events defined in the telemetry catalog/constants and through typed capture helpers.
- Don’t emit raw event strings where a rule is enforced.
- For sandboxed/third-party/plugin telemetry, follow that plugin’s own naming scheme and rely on the host to prefix/rename; ensure opt-out is honored.

2) Record terminal status/cause before tracing spans close
- If failures occur during streaming, ensure the error is recorded early enough that the integration can still update the generation/model-call spans.
- Add tests that assert terminal generation span status/exception (not just root spans).

3) Prevent stale attribution (reset per logical unit)
- Clear or recompute fields like “finishReason” / provider-failure details per *turn* (or per the unit of attribution) so a later failure can’t inherit an earlier one.
- When error types wrap/transform messages, don’t rely on brittle equality checks—add tests for those wrapped failure classes.

4) Classify reasons exactly (avoid metric inflation)
- Don’t reuse a generic stage for multiple distinct failure causes. If you emit `TIMEOUT`, it must correspond to a real timeout condition.
- If telemetry input was “ask failed” vs “stream timed out”, emit a dedicated reason/stage.

5) Avoid double counting—identify the single source of truth
- Before adding a new telemetry capture call, find whether a central runtime/event-adapter path already records that metric. Double emission should be treated as a bug.

6) Ensure observation timers can’t produce false samples
- If you arm a timer for detached/async observation, cancel/clear it on spawn/setup failure. Never report “ran for N ms” when the process never existed.

7) Protect privacy and keep telemetry non-blocking
- Never include prompt text, typed text, or sensitive hashes in telemetry events; drop/omit those fields.
- Telemetry capture should be failure-tolerant (telemetry adapter failures must not break inference).

Example pattern (lifecycle ordering + non-blocking capture)
```ts
// Terminal streaming telemetry: record before spans close; never throw.
let failedError: unknown | undefined;
function recordStreamError(err: unknown) {
  failedError = err;
}

function onProviderErrorChunk(err: unknown) {
  // mark failure early
  recordStreamError(err);
}

async function onProviderFinishChunk(finishReason: string) {
  if (finishReason === "error" && failedError !== undefined) {
    try {
      await recordError(failedError); // updates generation span while still open
    } finally {
      failedError = undefined;
    }
  }
}
```

Minimum required tests
- Assert the emitted event name (catalog constant / plugin prefix) and key properties.
- Assert correct terminal phase/cause and that stale attribution is impossible.
- Include at least one streaming and one misclassification/timer-false-sample regression test.