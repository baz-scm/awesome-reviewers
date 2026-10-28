---
title: Safe model-call retries
description: 'When a model call is retried, raced against a deadline, or recovered
  from truncation/overflow, treat every attempt as part of one logical call: never
  replay or lose tool-call side effects, and keep usage/cost telemetry correct across
  attempts.'
repository: cline/cline?x
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70983
---

When a model call is retried, raced against a deadline, or recovered from truncation/overflow, treat every attempt as part of one logical call: never replay or lose tool-call side effects, and keep usage/cost telemetry correct across attempts.

Specifically:
- Before retrying a stream or recovering from a truncated/overflowed turn, check for already-executed side effects (tool calls in message content, or provider-executed activity recorded in metadata, e.g. `metadata.modelToolActivities`). If any exist, do not silently discard them — preserve the completed tool results in history, or fall back to the original truncated/partial turn instead of re-issuing a request that would repeat file edits, commands, or other irreversible actions.
- Only retry on errors explicitly marked retryable by the provider/SDK; don't let a generic stream-retry path hide a non-retryable error behind several identical attempts. Prefer backoff over immediate retries for transient failures.
- Accumulate usage, cost, and first-token timing across all attempts of a logical call (including failed/aborted ones) into a single record, rather than dropping telemetry on a failed attempt or double-counting it after a retry succeeds. Close out any open telemetry span/trace for a failed attempt before starting the next one.
- When aggregating token usage, account for provider-specific shapes where some fields (e.g. reasoning tokens) are reported as a subset of another field (e.g. outputTokens) rather than additive, and add support for the specific nested shapes exercised by provider responses, with a regression test per shape.

Example pattern:
```ts
// Guard against replaying completed side effects before recovery/retry
if (hasModelToolActivity(turn.message) || turn.message.content.some(p => p.type === "tool-call")) {
  // preserve completed activity / fall back to the original turn
  return turn;
}
// Otherwise attempt recovery/retry, summing usage across every attempt
const meter = new CallMeter();
const retry = await issueRequest(meter);
```