---
title: Accurate, typed telemetry events
description: All new monitoring/telemetry events must be defined as typed catalog
  constants with dedicated capture helpers (e.g. `CORE_TELEMETRY_EVENTS.X.Y` plus
  a `captureX` helper in `core-events.ts`), not emitted as raw string literals with
  ad-hoc property bags scattered across call sites. This keeps event names, payload
  shapes, and consumers discoverable and...
repository: "cline/cline\t"
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 70947
---

All new monitoring/telemetry events must be defined as typed catalog constants with dedicated capture helpers (e.g. `CORE_TELEMETRY_EVENTS.X.Y` plus a `captureX` helper in `core-events.ts`), not emitted as raw string literals with ad-hoc property bags scattered across call sites. This keeps event names, payload shapes, and consumers discoverable and testable, and prevents silent drift when fields are renamed (a positional rename of `taskId` -> `ulid` that left call sites unchanged corrupted the recorded identifier without any compiler error).

Beyond typing, the signal itself must be correct:
- The reason/stage/outcome recorded must match the actual condition observed, not a nearby or convenient label. Don't report an empty-output condition as `TIMEOUT`, or any `ask` rejection as a `STREAM_TIMEOUT` hang — add a specific reason/stage instead of overloading an existing one, since merged categories make the metric useless for the purpose it was added for.
- Success/failure verdicts must reflect the real terminal state. A retried operation that errors, aborts, or is truncated again must not be recorded as succeeded; attach the actual finish reason/error type as data rather than a hand-wavy "completed" label, and make clear in the event semantics whether a phase is purely observational or an actual verdict (avoid duplicating or contradicting another component's decision).
- Diagnostics must be derived from the actual event/response that caused the failure, not inferred from a stale proxy (e.g. "last message in the transcript") that may not correspond to the failing turn.
- For tracing, make sure the terminal span of an operation is marked with its error before that span closes — reporting the failure later only updates still-open parent spans, leaving the specific failed unit unmarked in the trace.

Finally, instrument deliberately: don't add a parallel capture for something a central pipeline already instruments (e.g. tool-usage events emitted once via the existing event-adapter path) and don't ship a new event without a concrete consumption story — a dashboard, an investigation query, or a decision gate/tripwire — so each signal earns its ongoing cost.

Example pattern to follow:
```ts
// core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  SDK: { STREAM_RETRY: "sdk.stream_retry" },
} as const;

export function captureSdkStreamRetry(
  telemetry: ITelemetryService | undefined,
  props: { attempt: number; delayMs: number; providerId: string },
): void {
  telemetry?.capture({ event: CORE_TELEMETRY_EVENTS.SDK.STREAM_RETRY, properties: props });
}

// call site
captureSdkStreamRetry(context.telemetry, { attempt, delayMs, providerId });
```