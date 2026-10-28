---
title: Telemetry event integrity
description: 'Treat telemetry/tracing data as a product with correctness guarantees,
  not an afterthought bolted onto feature code:


  1. Register, don''t scatter: every new event/metric/counter name must be added to
  the central catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX`/`recordX`
  helper, instead of inlining raw string literals at the call site....'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 17
repository_stars: 70968
---

Treat telemetry/tracing data as a product with correctness guarantees, not an afterthought bolted onto feature code:

1. Register, don't scatter: every new event/metric/counter name must be added to the central catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX`/`recordX` helper, instead of inlining raw string literals at the call site. Add/extend the catalog-consistency test so drift is caught at compile/test time.
2. Justify before you instrument: a new event should have a stated consumer (a dashboard, a specific investigation query, or a tripwire alert) and a bounded, well-defined set of property values. Speculative "might be useful someday" events bloat the schema and are hard to act on.
3. Report the real condition, not a convenient label: pick the reason/stage/outcome code that actually matches what happened (e.g. don't report `TIMEOUT` for an empty-output case, or `STREAM_TIMEOUT` for any ask failure) and verify every call site after renaming a telemetry property or parameter — a positional rename that silently changes the semantic meaning of a value (e.g. passing a `taskId` under a `ulid` key) will compile but corrupt the data.
4. Cover every code path that represents real activity or state: if other paths are already wired to mark progress, success, or failure, make sure new/alternate paths (e.g. tool-call deltas, a second turn reusing stale state) feed the same signal, or detectors built on top of it (idle timers, health checks) will misfire. Conversely, don't add a second capture call for an event already emitted centrally — check existing instrumentation first to avoid double-counting.
5. Close what you open: for phased/lifecycle telemetry (`started` → `succeeded`/`failed`), guarantee every `started` emission is paired with a terminal phase on every exit path, including throws, aborts, and listener failures. Keep this telemetry strictly observational — record what happened (ran/retried/errored, with the real exception type) rather than re-deriving a success/failure verdict that the owning control-flow logic already computes; duplicating that judgment invites drift when the source logic changes.
6. For distributed tracing, attach error status/exceptions to the span that actually represents the failed operation before that span closes — a later, broader span update cannot repair an already-ended child span, so error-marking must happen on the terminal callback for that specific unit of work.

Example of the catalog pattern to follow for any new event:
```ts
// core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  SESSION: { PENDING_PROMPTS_DISCARDED: "session.pending_prompts_discarded" },
};
export function capturePendingPromptsDiscarded(
  telemetry: Telemetry | undefined,
  props: { sessionId: string; count: number; reason: string },
) {
  telemetry?.capture({
    event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
    properties: props, // never the raw prompt text
  });
}
```