---
title: Safe LLM stream retries
description: When adding retry, timeout, or recovery logic around streaming LLM calls,
  design for the realities of reasoning models and tool-executing providers rather
  than a one-size-fits-all timer or blind retry.
repository: "cline/cline\r\n"
label: AI
language: TypeScript
comments_count: 3
repository_stars: 70946
---

When adding retry, timeout, or recovery logic around streaming LLM calls, design for the realities of reasoning models and tool-executing providers rather than a one-size-fits-all timer or blind retry.

- Tune timeouts to actual streaming behavior: per-chunk/first-chunk timers that only reset on non-empty text/reasoning/tool-input deltas will falsely kill requests from models that "think" silently for a while before emitting anything. Don't reuse a short header-level timeout as a per-chunk timeout; give reasoning phases enough headroom (or disable the aggressive timer) so legitimate long-thinking runs aren't aborted as failures.
- Only retry a failed stream when the error is explicitly marked retryable, and prefer backing off rather than retrying immediately — immediate retries can exhaust attempts during a transient outage that a short backoff would have survived. Make sure request-level retry handling doesn't mask gaps in stream-level retry gating; verify with real HTTP-mocked tests that non-retryable stream errors don't still trigger multiple attempts.
- Never let a retry duplicate side effects. If a turn already executed a provider-owned tool, edited a file, or ran a command before the stream failed, guard against replaying that action — track completed tool/model activity (e.g. via message metadata) and use it to decide whether a retry is safe, and to preserve already-completed results when the retry itself partially succeeds before failing again.
- Close out telemetry/spans for an attempt before starting the next one, so retried or discarded attempts aren't silently dropped from traces.

Example pattern for gating a retry:
```ts
function canRetrySafely(error: StreamError, turn: TurnResult): boolean {
  if (!error.isRetryable) return false;
  if (hasModelToolActivity(turn.message)) return false; // already had side effects
  return true;
}
```
Apply backoff between attempts, preserve any completed tool activity from a partially-successful retry, and only fall back to a fresh/duplicate request when no safe alternative exists.