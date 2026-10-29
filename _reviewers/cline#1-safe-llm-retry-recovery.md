---
title: Safe LLM retry recovery
description: 'When a streamed model call fails, truncates, or times out, any automatic
  retry or recovery path must avoid corrupting conversation state or misreporting
  outcomes:'
repository: cline/cline#1
label: AI
language: TypeScript
comments_count: 6
repository_stars: 71024
---

When a streamed model call fails, truncates, or times out, any automatic retry or recovery path must avoid corrupting conversation state or misreporting outcomes:

- Never replay actions that already took effect. If a turn already executed tool calls, edited files, or produced provider-recorded tool activity (e.g. metadata like `modelToolActivities`), a retry must preserve that completed work rather than discarding it in favor of the earlier (now stale) turn.
- Only retry errors explicitly marked retryable, and apply backoff instead of immediate repeated attempts, so transient outages are given a chance to clear instead of exhausting retries instantly. Route recovery attempts through the same bounded provider-retry policy used elsewhere, rather than introducing a second, divergent retry mechanism.
- Timeouts and truncation heuristics (first-chunk timeouts, max-token recovery via compaction, etc.) must account for legitimate long-running model behavior — e.g. reasoning models that think silently before streaming — so recovery logic doesn't abort or "fix" a call that was actually healthy.
- Classify the final outcome of a retried/recovered turn using the same acceptance rules the run loop itself applies (e.g. a clean finish requires non-empty, renderable content; an aborted or errored retry is only "recovered" if it produced output the loop will actually accept). Telemetry/success metrics must mirror this real outcome, not just "the retry ran."
- Close out telemetry (spans, lifecycle events) for a failed attempt before starting the next one, so every retry is independently traceable.

Example shape to follow when adding recovery logic:
```ts
async function retryWithRecovery(first: Turn): Promise<Turn> {
  try {
    const retry = await attemptRetry(); // only when error.isRetryable, with backoff
    if (!loopAcceptsTurn(retry)) {
      await recordAssistantMessage(preserveCompletedActivity(first, retry));
      throw normalizeFailure(retry);
    }
    return retry;
  } catch (error) {
    closeTelemetrySpan(error);
    throw error;
  }
}
```