---
title: Telemetry Correctness Rules
description: 'Ensure observability data is accurate, non-misleading, and follows the
  project’s telemetry contracts.


  Apply these rules:

  1) Use typed/canonical event definitions'
repository: cline/cline#v13
label: Observability
language: TypeScript
comments_count: 14
repository_stars: 70874
---

Ensure observability data is accurate, non-misleading, and follows the project’s telemetry contracts.

Apply these rules:
1) Use typed/canonical event definitions
- Prefer central constants/catalog entries and typed helper APIs over raw event-name strings.
- Do not include prompt text or other sensitive/raw content in emitted telemetry.

2) Attribute failures to the right lifecycle moment
- Reset attribution fields (e.g., finish reason / last error cause) at the correct boundary (often per-turn, not per-run) to avoid stale telemetry.
- Don’t emit the wrong failure reason: if a failure is an ask error, timeout, overflow wrapper, etc., reflect that precisely.
- Ensure “started” telemetry always has a corresponding terminal phase, and that terminal status can’t be overwritten by a later/throwing hook.

3) Preserve tracing lifecycle ordering
- If a tracing span closes in one callback, ensure error information is delivered before that span ends (otherwise generation-level spans may remain “success/UNSET” while the overall operation fails).

4) Avoid double counting
- If tool usage/progress is captured centrally by the runtime/event adapter, don’t re-capture it in higher-level handlers.

5) Add tests that assert telemetry correctness
- Tests should verify specific event names/constants and required fields (counts, ids, reason enums, error types/statuses), plus ensure correct behavior for edge cases (unfinished items, recoveries that fail, streaming time thresholds).

Example pattern (typed/canonical + scoped properties + no raw payload):
```ts
// core-events.ts exposes a typed helper that targets a catalog constant
import { capturePendingPromptsDiscarded } from "./core-events";

function discardPendingPrompts(session: ActiveSession) {
  const discarded = pendingPromptsController.discardQueue(session);
  if (discarded.length === 0) return;

  capturePendingPromptsDiscarded({
    sessionId: session.sessionId,
    count: discarded.length,
    reason: "session_teardown",
    telemetry: session.config.telemetry,
  });
}
```

If you can’t point to (a) the typed/canonical event source, (b) the correct lifecycle boundary, and (c) a test that would fail if attribution/order/reason changes, don’t merge the observability change.