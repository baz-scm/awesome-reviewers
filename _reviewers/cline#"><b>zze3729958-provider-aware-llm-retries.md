---
title: Provider-aware LLM retries
description: When building retry, recovery, or usage-accounting logic around LLM providers,
  correctness must be driven by the provider's actual wire behavior, not assumptions,
  and must never duplicate or lose side effects from tool execution.
repository: cline/cline#"><b>zze3729958
label: AI
language: TypeScript
comments_count: 6
repository_stars: 71067
---

When building retry, recovery, or usage-accounting logic around LLM providers, correctness must be driven by the provider's actual wire behavior, not assumptions, and must never duplicate or lose side effects from tool execution.

- Never blindly retry or replay a turn that may have already executed irreversible actions (file edits, commands, provider-owned tool calls). Check whether tool activity already happened — including provider-executed tools recorded only in message metadata (e.g. `metadata.modelToolActivities`), not just `content` — before deciding a turn is safe to retry.
- When a recovery attempt (e.g. compaction-and-retry on max-tokens truncation) produces a partial result that still fails, preserve any completed tool activity from that attempt rather than discarding it and falling back to the original turn. Losing a completed tool result from history is a correctness bug, not just lost telemetry.
- Only honor an actually "retryable" classification from the provider/SDK before retrying; don't assume all stream or request errors are safe to retry immediately, and add backoff where immediate retries would exhaust transient outages.
- Scope any "facts about this turn" logic (edits made, errors seen, tool activity) strictly to the current turn/run span — don't let residual state from a prior turn (e.g. earlier edits or errors) leak into decisions like "should we retry" or "should we flag an error."
- Treat provider usage fields (token counts, reasoning tokens, nested shapes) as untrusted and version-specific: verify assumptions with wire-contract tests that exercise the real adapter/provider shape (not just a mocked constructor), and add a regression test for every newly discovered field shape (e.g. `outputTokens.reasoning` vs. provider metadata paths).
- Keep provider-specific quirks (e.g. Bedrock reasoning fields, Claude Code session recovery) isolated and tested at the integration boundary; prefer fixing them upstream in the adapter/SDK when a quirk is a bug in a third-party library rather than hard-coding a permanent workaround in core logic.

Example of preserving completed activity instead of discarding it on a failed retry:
```ts
// Bad: always falls back to the original truncated turn on any retry failure
if (retry.finishReason === "error") {
  return first;
}

// Good: only fall back when the retry produced no usable activity;
// otherwise keep the retry's completed tool results in history
if (retry.finishReason === "error" && !this.hasModelToolActivity(retry.message)) {
  await this.recordAssistantMessage(first.message, first.finishReason);
  throw error;
}
```