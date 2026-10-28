---
title: Accurate telemetry instrumentation
description: Telemetry/metrics instrumentation must faithfully represent the real
  condition it reports, and must be defined so that drift is caught, not silently
  shipped.
repository: cline/cline#中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中中
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70984
---

Telemetry/metrics instrumentation must faithfully represent the real condition it reports, and must be defined so that drift is caught, not silently shipped.

1. Emit events through typed, centralized catalog helpers (e.g. `CORE_TELEMETRY_EVENTS.*` with a `captureX` helper that takes named fields), never raw string-literal `capture({ event: "..." , properties: {...} })` calls scattered in business logic. Centralizing the schema means a field rename is compile-checked everywhere it's used — the opposite of what happened when `captureCheckpointUsage(taskId: string)` was renamed to `ulid` but call sites kept passing the task ID positionally and TypeScript happily compiled it, silently corrupting the property's meaning across events.

2. The reason/stage/outcome value captured must match the actual condition being measured, not a convenient default. Don't report `TIMEOUT` for an empty-output case, or a `STREAM_TIMEOUT` hang stage for any failed `ask()` call — introduce the specific enum value (`NO_OUTPUT`, `ASK_FAILED`, etc.) so the metric stays meaningful. Likewise, derive diagnostic fields (e.g. "what did the run end on") from the current turn/live state rather than a stale transcript tail or a previous turn's leftover field — reset per-turn/per-run state explicitly so a prior turn's `finishReason` can't leak into this turn's failure report.

3. Treat multi-phase telemetry (`started` → `succeeded`/`failed`) as a state machine: every `started` must get exactly one terminal phase, even on throw/abort paths, and "succeeded" must be gated on the actual success criteria (e.g. a clean `stop`/`tool-calls` finish) rather than "the retry didn't throw." Audit every exit path (including rethrows) to guarantee the terminal event fires.

4. Instrument once, at the single authoritative point in the pipeline (e.g. where usage/events already flow centrally), to avoid double-counting; and keep telemetry a reporter of facts rather than a second copy of control-flow decision logic that can drift from the real implementation.

Before adding a new event, confirm who/what will consume it and what decision it drives — otherwise it's dead instrumentation nobody can act on.