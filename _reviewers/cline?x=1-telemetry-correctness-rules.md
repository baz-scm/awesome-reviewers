---
title: Telemetry correctness rules
description: 'When adding/adjusting observability (metrics, telemetry events, tracing),
  ensure it is both policy-compliant and operationally accurate:


  - **Use typed helpers + a closed event catalog** (no ad-hoc raw event strings).
  Build/emit telemetry through shared capture helpers that enforce the schema, names,
  and allowed reason values; add tests that assert the...'
repository: cline/cline?x=1
label: Observability
language: TypeScript
comments_count: 12
repository_stars: 70861
---

When adding/adjusting observability (metrics, telemetry events, tracing), ensure it is both policy-compliant and operationally accurate:

- **Use typed helpers + a closed event catalog** (no ad-hoc raw event strings). Build/emit telemetry through shared capture helpers that enforce the schema, names, and allowed reason values; add tests that assert the exact payload shape.
- **Respect user opt-out**: telemetry helper logic must not invoke “required” capture paths when disabled; verify with regression tests.
- **Never emit sensitive payloads**: queued/discarded/error telemetry should include counts/ids/reasons only—never prompt text or other raw content.
- **Emit at the correct lifecycle time**: for tracing, deliver error/failure data before the span/generation observation closes, or downstream analysis will show UNSET/missing exceptions.
- **Prevent wrong/stale attribution**: initialize/reset per-turn or per-attempt failure/cause fields so a later failure doesn’t inherit an earlier turn’s reason.
- **Use reason taxonomy that matches reality**: don’t collapse distinct conditions into a single label (e.g., TIMEOUT vs empty output; stream timeout vs generic ask failure) to avoid metric inflation.
- **Avoid double counting**: follow the central instrumentation pipeline (emit once, at the source or via adapters) and add tests that assert event cardinality (e.g., “exactly one”).
- **Make sampling windows truthful**: cancel/detach timers on spawn failures or early exits so you don’t report fabricated runtime samples.

Example pattern for discard-only telemetry (counts/reason/ids, typed helper, opt-out safe):
```ts
// core-events.ts
export function capturePendingPromptsDiscarded(
  telemetry: ITelemetryService | undefined,
  details: { sessionId: string; count: number; reason: 'queue_abort' | 'session_teardown' },
): void {
  emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
}

// caller
private discardPendingPrompts(session: ActiveSession, reason: 'queue_abort' | 'session_teardown') {
  const discarded = this.pendingPromptsController.discardQueue(session);
  if (discarded.length === 0) return;
  capturePendingPromptsDiscarded(this.telemetryService, {
    sessionId: session.sessionId,
    count: discarded.length,
    reason,
  });
}
```
