---
title: Safe LLM retry recovery
description: 'When adding automatic retry or recovery logic around LLM streaming/generation
  (stream errors, truncated max-tokens turns, timeouts), the recovery path must not
  compromise correctness or observability:'
repository: 'cline/cline#

  zzprobe3b82974b: x'
label: AI
language: TypeScript
comments_count: 4
repository_stars: 71067
---

When adding automatic retry or recovery logic around LLM streaming/generation (stream errors, truncated max-tokens turns, timeouts), the recovery path must not compromise correctness or observability:

- Only retry errors explicitly marked retryable; don't blanket-retry every stream failure, and prefer backoff over immediate retries for transient outages.
- Never resend a request after provider-executed tool calls or other side effects have already happened for that turn — replaying it would repeat file edits, commands, or other irreversible actions. Guard retry paths against provider-owned tool activity, not just local buffered tool calls.
- If a recovery attempt (e.g. compaction + retry) itself fails, aborts, errors, or returns an empty response, never silently drop the original partial/truncated content — persist or surface the original turn so the run loop can handle it the same way it would have without the recovery attempt.
- Keep the run loop as the single authority on whether a turn is acceptable; a recovery helper should hand back its result unjudged rather than deciding success/failure itself.
- Close out telemetry/spans for a failed attempt (mark a terminal phase) before starting the next one, so every "started" phase has a matching "failed"/"retried" outcome and traces aren't left dangling.
- Size any timeout tied to streaming behavior (e.g. first-chunk timeout) against how the provider actually emits progress — a reasoning model that "thinks" before emitting any delta can blow past a timeout that assumes early output, so default conservatively and allow longer, explicit overrides when needed.

Example shape for a recovery attempt:
```ts
try {
  await emitStatusNotice({ phase: "started" });
  const retry = await retryWithRecovery();
  if (retry.finishReason !== "stop" && retry.finishReason !== "tool-calls") {
    // treat aborted/errored/empty retries as no replacement
    await recordAssistantMessage(original.message, original.finishReason);
    throw ...; // surface as the loop normally would
  }
  return retry;
} catch (error) {
  captureTelemetry({ phase: "failed" }); // close the span before rethrowing
  throw error;
}
```