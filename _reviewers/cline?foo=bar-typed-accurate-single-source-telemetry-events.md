---
title: Typed, accurate, single-source telemetry events
description: Telemetry/metrics must never be emitted as ad-hoc raw strings scattered
  through the codebase. Every event name and its property shape should be defined
  once in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS.<DOMAIN>.<NAME>`) with a
  typed `captureX` helper that callers invoke instead of building the event object
  inline. This keeps event names, property...
repository: cline/cline?foo=bar
label: Observability
language: TypeScript
comments_count: 7
repository_stars: 71082
---

Telemetry/metrics must never be emitted as ad-hoc raw strings scattered through the codebase. Every event name and its property shape should be defined once in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS.<DOMAIN>.<NAME>`) with a typed `captureX` helper that callers invoke instead of building the event object inline. This keeps event names, property keys, and value types consistent across the whole system and lets a single test assert the catalog entry and helper shape rather than relying on call sites to stay in sync.

When a helper's parameter or property is renamed (e.g. `taskId` → `ulid`), audit and update every call site — positional renames compile but silently send the wrong value under the new key, corrupting cross-event joins. Add/adjust tests at the call sites, not just the helper.

Reason/outcome codes attached to an event must map 1:1 to the condition that actually occurred. Don't reuse a generic bucket (e.g. `TIMEOUT`, `STREAM_TIMEOUT`) for a different failure mode (e.g. empty output, a generic ask failure) just because it's convenient — add a distinct enum value instead, otherwise the resulting metric is too noisy to act on.

Instrument each user action or lifecycle transition exactly once, at the single, central point in the pipeline that already sees the canonical result (e.g. a shared event adapter), so adding a second capture call elsewhere doesn't double-count. Write a regression test that asserts the event fires exactly one time end-to-end.

Example:
```ts
// shared/core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  SESSION: { PENDING_PROMPTS_DISCARDED: "session.pending_prompts_discarded" },
};

export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  props: { sessionId: string; count: number; reason: string },
): void {
  telemetry?.capture({
    event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
    properties: props, // never raw prompt text
  });
}

// caller
capturePendingPromptsDiscarded(session.config.telemetry, {
  sessionId: session.id,
  count: discarded.length,
  reason: "session_teardown",
});
```

Apply this standard whenever adding or modifying telemetry: define/extend the catalog entry and helper, update every call site after a rename, pick a reason code that matches the real condition, and verify there is exactly one instrumentation point with a test.