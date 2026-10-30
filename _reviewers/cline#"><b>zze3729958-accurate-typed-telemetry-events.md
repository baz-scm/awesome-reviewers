---
title: Accurate typed telemetry events
description: 'Telemetry is only useful if it is both structurally consistent and truthful
  about what happened, so two rules apply to every new metric:


  1. Never capture with a raw string literal. Define the event name as a typed constant
  in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS.<DOMAIN>.<NAME>`) and add a typed
  `captureX` helper that pins the property shape,...'
repository: cline/cline#"><b>zze3729958
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 71067
---

Telemetry is only useful if it is both structurally consistent and truthful about what happened, so two rules apply to every new metric:

1. Never capture with a raw string literal. Define the event name as a typed constant in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS.<DOMAIN>.<NAME>`) and add a typed `captureX` helper that pins the property shape, then call that helper from call sites. This keeps event names/properties greppable and testable across packages, e.g.:
```ts
// core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  SESSION: { PENDING_PROMPTS_DISCARDED: "session.pending_prompts_discarded" },
};
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  props: { sessionId: string; count: number; reason: string },
) { telemetry?.capture({ event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, properties: props }); }
```
Before adding a brand-new event, confirm it has a concrete use (a dashboard, a specific investigation query, or a tripwire), and keep its properties a closed, bounded set — don't ship an event "just in case."

2. The captured data must match the real condition, not an approximation of it. Derive reasons/stages/outcomes from the actual code path that produced them rather than reusing a nearby catch block or a convenient but stale piece of state:
   - Give each distinct failure mode its own reason/stage value instead of forcing unrelated cases into an existing one (e.g. don't report `TIMEOUT` for an empty-output condition, or classify every `ask` rejection as a `STREAM_TIMEOUT` hang).
   - Classify success/failure against the same decision logic the system itself uses to accept or reject a result; a retry that errors, aborts, or is rejected downstream must not be recorded as "succeeded" just because it reached a terminal callback.
   - When renaming or restructuring a property, update every call site (rename is often positional, so the compiler won't catch a stale argument), and verify property semantics stay consistent across all events that share a name.
   - Instrument once, at the single authoritative point (e.g. a central event-adapter), and audit for double-counting if a new capture is being added near existing instrumentation.
   - Only count the user-initiated/representative case the metric claims to measure (e.g. don't count internal plumbing invocations as "activation").

Add or extend a test asserting the exact catalog constant/property values whenever telemetry is added or changed, so drift between the emitted event and its documented meaning is caught in review, not in the dashboard.