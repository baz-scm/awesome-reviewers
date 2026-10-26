---
title: Test Seams and Stability
description: 'When adding/updating tests, choose seams and assertions that protect
  real behavior without making the suite brittle.


  - Pick the right level for the risk'
repository: cline/cline#v7
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 70865
---

When adding/updating tests, choose seams and assertions that protect real behavior without making the suite brittle.

- Pick the right level for the risk
  - Unit tests: assert stable contract/policy behavior (e.g., exact telemetry payload shape; ensure disabled/opt-out paths don’t call dependent helpers).
  - “Wire”/adapter tests: when integration/wiring can break (e.g., request URL/body mapping), drive through the real adapter with only external I/O stubbed.
  - Real/integration checks: if mocking would require heavy process/shell plumbing that’s cross-platform fragile, validate with real runs and existing correctness coverage.

- Assert behavior, not churny internals
  - Prefer assertions on deterministic payloads/outputs/events.
  - Avoid locking onto log field-name shapes unless the suite already has a stable harness; rely on existing tests that exercise the path.

- Keep tests clean and non-leaky
  - Stub at the correct seam so async listeners/streams don’t outlive the test (avoid never-ending streams when you only need “reveal” semantics).
  - Manage env safely using test utilities (stub + restore/cleanup that works whether the variable was set or unset).

- Don’t let tests be too permissive
  - If a test approach can accidentally allow missing required groups (e.g., plural categories), tighten it to enforce the needed completeness based on the spec (e.g., CLDR cardinal categories).

Example pattern (contract shape + opt-out):
```ts
// Disabled adapter should never trigger follow-up capture
expect(disabledAdapter.capture).toHaveBeenCalledTimes(1);
expect(disabledAdapter.capture).toHaveBeenCalledWith(
  CORE_TELEMETRY_EVENTS.SESSION.PENDING_PROMPTS_DISCARDED,
  { sessionId: "s1", count: 3, reason: "queue_abort" },
);
expect(disabledAdapter.captureRequired).not.toHaveBeenCalled();
```

Use this standard to make tests both meaningful (catching real regressions) and stable (minimizing brittle harness and churn).