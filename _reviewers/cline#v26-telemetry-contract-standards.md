---
title: Telemetry Contract Standards
description: 'Adopt a single telemetry contract for all observability code: emit only
  through typed, cataloged helpers; ensure lifecycle ordering and correct attribution;
  sanitize/redact; and guarantee telemetry is non-interfering and opt-out safe.'
repository: cline/cline#v26
label: Observability
language: TypeScript
comments_count: 17
repository_stars: 70893
---

Adopt a single telemetry contract for all observability code: emit only through typed, cataloged helpers; ensure lifecycle ordering and correct attribution; sanitize/redact; and guarantee telemetry is non-interfering and opt-out safe.

Guidelines
- Use typed helpers + catalog constants for first-party events (avoid raw event-name strings). Keep shapes consistent and test them.
  - Example pattern:
    ```ts
    // core-events.ts
    export function capturePendingPromptsDiscarded(
      telemetry: ITelemetryService | undefined,
      details: { sessionId: string; count: number; reason: 'queue_abort'|'session_teardown' },
    ): void {
      emit(telemetry, CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED, details);
    }

    // call site
    session.config.telemetry?.capture({ event: /* use helper */ }); // instead of ad-hoc raw capture
    capturePendingPromptsDiscarded(session.config.telemetry, { sessionId, count, reason });
    ```
- Never let telemetry break behavior: wrap captures in try/catch, and ensure “never throws” semantics.
- Respect opt-out: tests should verify helpers don’t call expensive/side-effectful paths when telemetry is disabled.
- Sanitize/redact: never export prompt text, secrets, credentials, raw remotes, or hashed prompt fields. Drop/transform fields before they leave the process.
- Correct attribution & lifecycle ordering:
  - Reset attribution per turn (avoid stale finish/reason/causes bleeding into later failures).
  - Ensure errors are reported before tracing spans/generation lifecycles close; if an error notification arrives “too late”, assert terminal span status/exception explicitly in tests.
- Preserve metric integrity:
  - Emit precise reason taxonomies (don’t overload TIMEOUT/empty-output or ask-error/hang).
  - Avoid double-counting by using the established central instrumentation pipeline rather than adding extra captures in adapters/handlers.
- Write tests that lock the telemetry contract:
  - Event name must match the catalog constant.
  - Payload shape must match exactly (including “no prompt text” constraints).
  - Disabled-adapter opt-out behavior must be asserted.
  - Add coverage for long streaming/progress thresholds and for retry/success/failure correctness.

This standard prevents the common observability regressions seen in practice: stale/incorrect cause attribution, terminal-span misses due to late error reporting, metric poisoning from misclassified reasons, double counting, and privacy leaks or opt-out violations.