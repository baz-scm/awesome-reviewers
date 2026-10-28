---
title: Accurate typed telemetry events
description: 'Telemetry is only useful if it is typed, complete, and matches the real
  condition it claims to describe. When adding or editing instrumentation:


  1. Never emit raw literal event strings for first-party code. Register the event
  in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) and add a typed `captureX`/`recordX`
  helper so the event name, shape, and call...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70976
---

Telemetry is only useful if it is typed, complete, and matches the real condition it claims to describe. When adding or editing instrumentation:

1. Never emit raw literal event strings for first-party code. Register the event in the shared catalog (e.g. `CORE_TELEMETRY_EVENTS`) and add a typed `captureX`/`recordX` helper so the event name, shape, and call sites stay in sync and are tested against the catalog constant.

```ts
// Bad
config.telemetry?.capture({ event: "session.pending_prompts_discarded", properties: { sessionId, count, reason } });

// Good
export const CORE_TELEMETRY_EVENTS = {
  SESSION: { PENDING_PROMPTS_DISCARDED: "session.pending_prompts_discarded" },
};
export function capturePendingPromptsDiscarded(telemetry, props: { sessionId: string; count: number; reason: string }) {
  telemetry?.capture({ event: CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, properties: props });
}
```

2. Classify failure/stage reasons by the actual observed condition, not by the code path's name or an assumption. An "empty output" result is not a `TIMEOUT`, and a generic `ask()` rejection is not necessarily a `STREAM_TIMEOUT` hang — add a distinct reason/stage rather than overloading an existing one, or the resulting metric becomes meaningless.

3. For multi-phase/lifecycle telemetry (e.g. `started` → `succeeded`/`failed`), guarantee every `started` emission reaches exactly one terminal phase, including on throw, abort, or a downstream listener error. Capture the terminal status (and attach the error) on the actual object being closed — e.g. the terminal span/generation — before it closes, not in a later handler that can no longer update it. Keep this instrumentation observational: it should report what happened, not re-derive or contradict the verdict the business logic (e.g. the run loop) already owns, to avoid duplicated or conflicting success/failure judgments.

4. Before adding a capture call, check whether a central pipeline (e.g. a shared event adapter) already instruments that action; adding a second call site causes double-counting.

5. Make sure progress/health signals observe every kind of real activity (including streamed deltas), not just a subset of event types, so idle/hang detection isn't triggered by activity it failed to see.

Apply these checks whenever adding, renaming, or refactoring telemetry so dashboards and alerts stay trustworthy.