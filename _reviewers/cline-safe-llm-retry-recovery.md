---
title: Safe LLM retry recovery
description: 'When adding retry, continuation, or recovery logic around LLM streaming
  responses (stream errors, max-tokens truncation, degenerate/incomplete output, etc.),
  never silently discard work that already happened or is still pending delivery.
  Before issuing a retry: confirm the underlying error is actually marked retryable
  and back off appropriately rather than...'
repository: cline/cline
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70886
---

When adding retry, continuation, or recovery logic around LLM streaming responses (stream errors, max-tokens truncation, degenerate/incomplete output, etc.), never silently discard work that already happened or is still pending delivery. Before issuing a retry: confirm the underlying error is actually marked retryable and back off appropriately rather than hammering immediately; preserve provider-executed tool activity and completed tool calls recorded in message metadata so a later retry doesn't drop or duplicate real side effects; and if a recovery attempt fails or aborts, fall back to persisting the original (possibly partial) turn rather than losing it. Close out any in-flight telemetry/tracing spans for the failed attempt before starting a new one so retried attempts remain visible in traces. Because providers and SDKs differ subtly in how they buffer, replay, or signal retryability (e.g. Bedrock vs. Anthropic vs. local OpenAI-compatible servers), add wire-level tests against the real provider adapter rather than relying on assumptions about its behavior, and when a quirk is provider-specific, prefer isolating/documenting it (or fixing it upstream) over baking special cases into shared code paths.

Example pitfall to avoid:
```ts
// BAD: retries a failed stream and discards any completed tool activity
// recorded in metadata, risking duplicated side effects or lost results.
catch (error) {
  return await retryStream(request); // drops `first.message.metadata.modelToolActivities`
}

// GOOD: only retry when safe, and preserve completed activity either way
catch (error) {
  if (!isRetryable(error)) {
    await recordAssistantMessage(first.message, first.finishReason);
    throw error;
  }
  const retry = await retryStream(request);
  return mergeCompletedToolActivity(first, retry);
}
```