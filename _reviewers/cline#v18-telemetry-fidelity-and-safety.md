---
title: Telemetry fidelity and safety
description: 'Treat telemetry as a correctness-sensitive product: if you can’t guarantee
  accurate classification, safe content, and correct lifecycle ordering, don’t emit
  it.'
repository: cline/cline#v18
label: Observability
language: TypeScript
comments_count: 10
repository_stars: 70884
---

Treat telemetry as a correctness-sensitive product: if you can’t guarantee accurate classification, safe content, and correct lifecycle ordering, don’t emit it.

**Coding standard**
1) **Use typed, cataloged event APIs (where applicable)**
- Prefer constants/helpers for event names and property schemas.
- Avoid raw/unscoped event-name strings in areas with strict catalogs.

2) **Drop sensitive/unsafe fields by construction**
- Never include prompt text (or hashed prompt equivalents) in exported telemetry payloads.
- Do not forward local stderr that may contain paths/remotes/credentials.

3) **Classify reasons with one-to-one meaning**
- Reason enums must match the actual condition (e.g., `NO_OUTPUT` vs `TIMEOUT`, `ASK_FAILED` vs “hang due to stream timeout”).
- Don’t merge distinct failure modes into a single reason.

4) **Reset attribution at the correct lifecycle boundary**
- Failure causes (finishReason/error details) must be cleared/reset per unit (e.g., per **turn**, not per run) before any fallible work.
- Prevent “stale” causes from being reported on later failures.

5) **Capture before traces/spans close**
- For streaming/tracing, ensure error reporting happens early enough that the relevant span can be marked with the exception before it ends.

6) **Avoid double counting**
- If a central pipeline already emits an event (e.g., task/tool usage), do not re-emit the same metric in downstream handlers.

**Illustrative pattern (typed helper + safe properties + correct ordering)**
```ts
// Typed constants/helpers (core scope):
// import { CORE_TELEMETRY_EVENTS } from "./catalog";
// import { capturePendingPromptsDiscarded } from "./core-events";

function captureEventOnce(
  telemetry: { isEnabled(): boolean; capture(x: { event: string; properties?: any }): void } | undefined,
  sessionId: string,
  count: number,
  reason: "queue_abort" | "session_teardown",
) {
  if (!telemetry?.isEnabled()) return;

  // Closed-set reasons + safe properties: no prompt text/hash.
  telemetry.capture({
    event: "SESSION.PENDING_PROMPTS_DISCARDED", // use the typed constant/helper in real code
    properties: { sessionId, count, reason },
  });
}

// Stream/tracing: record error before the generation span ends.
// Ensure terminal capture occurs in the correct callback order (not “too late”).
async function onStreamTerminal(error: unknown, recordError: (e: unknown) => Promise<void>) {
  // Call recordError before letting the tracer lifecycle close the generation observation.
  await recordError(error);
}
```

**Checklist for PRs**
- Can the event’s name/reason be wrong? (If yes, don’t emit or gate it.)
- Are properties sanitized (no prompt text, hashes, credentials/paths)?
- Is attribution reset at the right boundary (turn vs run)?
- Is the telemetry emitted before relevant spans end?
- Could this event be double-counted by an existing central pipeline?