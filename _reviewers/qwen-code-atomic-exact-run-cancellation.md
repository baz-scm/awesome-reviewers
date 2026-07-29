---
title: Atomic Exact-Run Cancellation
description: When implementing concurrent async workflows with callbacks (Stop/Submit/Cancel,
  permission settlement, card actions), make the operation safe against stale/foreign/parallel
  events by using atomic identity validation plus a synchronous “claim” before any
  awaited side effects.
repository: QwenLM/qwen-code
label: Concurrency
language: Markdown
comments_count: 7
repository_stars: 26407
---

When implementing concurrent async workflows with callbacks (Stop/Submit/Cancel, permission settlement, card actions), make the operation safe against stale/foreign/parallel events by using atomic identity validation plus a synchronous “claim” before any awaited side effects.

Apply these rules:
- Use opaque per-invocation identifiers (e.g., runId/requestId) generated per prompt/request; never rely on session lifecycle counters that don’t change per run.
- For exact-run actions (like Stop), validate an expected runId against the current active prompt atomically in the owning layer. If missing/stale/mismatched, reject without any session-only fallback.
- Use an adapter-local in-flight claim/lock keyed by the exact record (runId/outTrackId). Claim synchronously and only allow the async path that holds the claim to mutate/update/release.
- Define deterministic state-machine behavior under concurrency:
  - Track all pending request IDs for the run and derive “waiting for input” from the full set.
  - Terminal lifecycle states must take precedence over non-terminal updates.
- External callback acknowledgment should happen after parsing/correlation/owner validation and the synchronous claim, but before awaiting slow operations (don’t leave the transport ack pending across awaits).

Example (pattern for exact-run Stop):
```ts
async function cancelRunFromCard(expectedRunId: string, ownerKey: OwnerKey): Promise<boolean> {
  // 1) parse/validate owner + callback identity (no awaits yet)
  if (!isOwnerMatch(ownerKey)) return false;

  // 2) synchronous claim of the current live record
  const active = getCurrentActivePrompt(); // atomic read
  if (!active || active.runId !== expectedRunId) return false;
  const claim = tryClaim(active); // must be synchronous
  if (!claim) return false;

  // 3) only now do awaited side effects
  const ok = await channelBase.cancelExactRun(active.sessionId, expectedRunId);
  if (ok) {
    blockNewStreamingChunks(active.runId);
    commitStoppedProjection();
    claim.releaseSuccess();
  } else {
    claim.release(); // keep card active for retry
  }
  return ok;
}
```
Adopt this as a standard for any callback-driven cancellation/submission path so parallel runs and near-simultaneous callbacks cannot corrupt state or show incorrect success to users.