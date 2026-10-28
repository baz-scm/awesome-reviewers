---
title: Cataloged, accurate telemetry
description: Every telemetry/trace event must be declared once in the shared event
  catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX` helper, instead of
  being emitted as an ad-hoc string literal at the call site. This keeps event names,
  property shapes, and PII handling (e.g. never logging raw prompt text) consistent
  and discoverable, and is enforced by...
repository: cline/cline#|sleep 4
label: Observability
language: TypeScript
comments_count: 16
repository_stars: 70979
---

Every telemetry/trace event must be declared once in the shared event catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX` helper, instead of being emitted as an ad-hoc string literal at the call site. This keeps event names, property shapes, and PII handling (e.g. never logging raw prompt text) consistent and discoverable, and is enforced by catalog-consistency tests.

```ts
// core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  SESSION: { PENDING_PROMPTS_DISCARDED: "session.pending_prompts_discarded" },
};
export function capturePendingPromptsDiscarded(telemetry, { sessionId, count, reason }) {
  telemetry?.capture({
    event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
    properties: { sessionId, count, reason },
  });
}
```

Beyond structure, the captured data must be *true to the condition it claims to describe*:

- Reason/stage/outcome codes must map 1:1 to the actual branch that fired them — don't report `TIMEOUT` for an empty-output path or `STREAM_TIMEOUT` for any ask failure; add a distinct enum value instead of overloading an existing one.
- Success/failure verdicts must reflect the real terminal state: only a cleanly finished operation counts as success; mark terminal spans/observations with their error before the lifecycle that owns them closes (not after, in a later hook that can no longer touch the already-ended span); if a listener throws while emitting the terminal notice, the telemetry must still record failure before the error propagates.
- Don't duplicate classification logic (e.g. "was this run aborted vs failed") in a secondary telemetry path — that copy drifts from the single source of truth owned by the main control flow. Prefer having the secondary path report only raw, unambiguous facts (what ran, what exception type was observed) and let the owning code's outcome be joined separately.
- Watch for blind spots in instrumentation coverage (e.g. a progress/liveness signal that isn't updated by every code path that represents real progress) and for double-counting (e.g. an "activation" event firing for internal plumbing calls, not just genuine user actions).
- When renaming or restructuring an event's properties, audit and update every call site — a positional rename (e.g. `taskId` → `ulid`) can compile cleanly while silently mixing two different identifier formats under the same property key across events.

Before adding a new event, state what question or action it enables (dashboard, debugging query, tripwire) and keep its volume/shape bounded to that need; this makes it easy to judge whether the event is worth keeping or should be removed once its question is answered.