---
title: Telemetry event discipline
description: Treat telemetry events as a maintained API, not ad-hoc capture calls.
  Register every new event/metric name as a constant in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`)
  with a typed `captureX`/`recordX` helper that fixes the property shape, and cover
  it with the catalog-consistency test — never call `capture()` with a raw string
  literal or an untyped...
repository: cline/cline#zzz-unlikely-123abc
label: Observability
language: TypeScript
comments_count: 11
repository_stars: 71035
---

Treat telemetry events as a maintained API, not ad-hoc capture calls. Register every new event/metric name as a constant in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) with a typed `captureX`/`recordX` helper that fixes the property shape, and cover it with the catalog-consistency test — never call `capture()` with a raw string literal or an untyped payload. When renaming a property on an existing helper (e.g. `taskId` → `ulid`), audit and update every call site in the same change, since positional arguments compile silently and can leave two incompatible value formats under one key. Before adding an event, write down the concrete question, dashboard, or alert it serves (e.g. "how often does recovery X actually fix Y") so events aren't shipped speculatively and left unused. Keep events accurate to what actually happened: classify failures by real cause instead of lumping distinct errors under one coarse stage (don't tag every ask-failure as a `STREAM_TIMEOUT` hang), derive status/diagnostic fields from the current turn or outcome rather than stale state carried from a prior turn or transcript tail, and only mark an operation "succeeded" when it truly completed as intended (an errored/aborted/truncated-again retry must record failure, not success). Finally, keep telemetry purely observational where a decision is already owned elsewhere — report what happened (e.g. "retried", with the observed finish reason) rather than re-deriving a success/failure verdict that duplicates logic in the main control path, since duplicated judgment drifts out of sync over time.

Example of a typed, catalog-registered event instead of an ad-hoc capture:
```ts
// shared/telemetry.ts
export const TASK_MAX_TOKENS_RECOVERY_EVENT = "task.max_tokens_recovery";

// core-events.ts
export const CORE_TELEMETRY_EVENTS = {
  TASK: { MAX_TOKENS_RECOVERY: TASK_MAX_TOKENS_RECOVERY_EVENT, /* ... */ },
};

export function captureMaxTokensRecovery(props: {
  phase: "started" | "retried" | "failed";
  eventType?: string;
}) {
  telemetry.capture({ event: CORE_TELEMETRY_EVENTS.TASK.MAX_TOKENS_RECOVERY, properties: props });
}
```