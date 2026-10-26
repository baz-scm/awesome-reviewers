---
title: Observability Semantic Contract
description: Ensure all telemetry/tracing is (1) contract-compliant, (2) semantically
  correct, and (3) recorded at the right point in each lifecycle—backed by targeted
  regression tests.
repository: cline/cline#v11
label: Observability
language: TypeScript
comments_count: 8
repository_stars: 70871
---

Ensure all telemetry/tracing is (1) contract-compliant, (2) semantically correct, and (3) recorded at the right point in each lifecycle—backed by targeted regression tests.

**Rules**
1. **Use typed event helpers / catalog constants**
   - Prefer centralized, typed capture helpers over ad-hoc string literals.
   - Scope enforcement: if an event name rule is scoped to first-party packages, don’t force core-catalog entries for sandboxed plugins that are remapped by the host.
   - **Sanitize**: never include raw prompt text/hashes in telemetry payloads.
   - **Test**: assert the emitted event name/property keys against the catalog/constant.

2. **Classify failures with distinct reasons**
   - Don’t collapse distinct conditions into one metric label (e.g., timeout vs empty output).
   - If the observable category can be wrong (e.g., “hang” emitted on any ask failure), introduce a dedicated reason/stage or gate emission to the true condition.

3. **Attribute causes at the correct scope (turn vs run)**
   - Clear/retain attribution based on the actual lifecycle boundary.
   - Preserve wrapped/high-signal error details for specific error classes (e.g., avoid clearing provider details when the error is wrapped and message equality won’t hold).

4. **Record errors before trace spans close**
   - If an integration can close generation/step spans before later stream callbacks arrive, capture/mark the error early (or propagate it into the lifecycle that’s still open).
   - **Test** exported spans’ status/exception at the generation span level, not only the root/span.

5. **Telemetry wiring must not mutate session bootstrap truth**
   - Attaching telemetry should not rewrite session identifiers or other fields that change core behavior (e.g., restart/read-only resume detection).

**Example (pattern)**
```ts
// Prefer a typed helper + safe properties
import { CORE_TELEMETRY_EVENTS, capturePendingPromptsDiscarded } from "./core-events";

function discardPendingPrompts(session: ActiveSession, reason: "queue_abort" | "session_teardown") {
  const discarded = pendingPromptsController.discardQueue(session);
  if (discarded.length === 0) return;

  // Never include prompt text; only ids/counts/reason
  capturePendingPromptsDiscarded({
    sessionId: session.sessionId,
    count: discarded.length,
    reason,
  });
}

// Tracing: mark failure before lifecycle ends
async function onTerminalChunk(chunk: StreamChunk, lifecycle: { onEnd: (e: any)=>Promise<void> }) {
  if (chunk.type === "error") {
    // Ensure generation span status is updated while generation is still open
    telemetrySpan.markError(chunk.error);
  }
  await lifecycle.onEnd({ finishReason: "error" });
}
```

**What to look for in reviews**
- Are event names/constants centralized and tested?
- Are payloads sanitized and stable (no raw text)?
- Are failure reasons/stages distinct and non-inflating?
- Are error causes attributed to the correct lifecycle boundary?
- For tracing: do tests assert generation/step spans are marked with exceptions/status when expected?
- Does telemetry attachment avoid mutating core session semantics?