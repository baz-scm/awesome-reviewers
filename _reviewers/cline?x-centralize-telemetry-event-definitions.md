---
title: Centralize telemetry event definitions
description: 'Define every telemetry signal (event, counter, histogram) once in the
  shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX`/`recordX`
  helper, and call that helper everywhere the signal fires. Do not emit ad-hoc string
  literals (`telemetry.capture({ event: "session.pending_prompts_discarded", ... })`)
  inline — register the constant and helper...'
repository: cline/cline?x
label: Observability
language: TypeScript
comments_count: 8
repository_stars: 70983
---

Define every telemetry signal (event, counter, histogram) once in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX`/`recordX` helper, and call that helper everywhere the signal fires. Do not emit ad-hoc string literals (`telemetry.capture({ event: "session.pending_prompts_discarded", ... })`) inline — register the constant and helper first, add a catalog-consistency test, and call the helper from the call site instead:

```ts
// shared/core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  SESSION: { PENDING_PROMPTS_DISCARDED: "session.pending_prompts_discarded" },
};
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  props: { sessionId: string; count: number; reason: string },
) {
  telemetry?.capture({
    event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
    properties: props,
  });
}
```

This gives one source of truth for names/properties, lets a lint rule and tests catch drift, and keeps instrumentation honest: don't collapse distinguishable outcomes into a reused reason/stage value for convenience (an "empty output" condition should not be reported as `TIMEOUT`, and a generic `ask` failure should not be classified as a stream-timeout hang) — add the specific enum value the condition actually needs. Also check whether the occurrence is already captured by a central pipeline (e.g. a shared event adapter already emitting `task.tool_used`) before adding a second capture call for the same event, to avoid double-counting metrics. Code that is sandboxed or proxies through a host's own telemetry service (examples/plugins) is exempt from the first-party catalog, since its events are renamed/namespaced by the host and never match the core catalog anyway.