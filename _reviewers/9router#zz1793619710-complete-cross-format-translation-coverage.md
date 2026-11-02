---
title: Complete cross-format translation coverage
description: When translating requests/responses between provider-native shapes (OpenAI,
  Claude, Responses, Gemini, Zed, etc.) and client-facing formats, treat every translation
  path as part of the public API contract and verify it end-to-end for every client
  format and transport mode (streaming and non-streaming).
repository: decolua/9router#zz1793619710
label: API
language: JavaScript
comments_count: 5
repository_stars: 31855
---

When translating requests/responses between provider-native shapes (OpenAI, Claude, Responses, Gemini, Zed, etc.) and client-facing formats, treat every translation path as part of the public API contract and verify it end-to-end for every client format and transport mode (streaming and non-streaming).

Concretely:
- Explicitly declare per-model/per-provider capabilities (e.g. `supportedFormats`) instead of relying on implicit/null defaults to pick an endpoint transport; an unlisted or ambiguous capability should fail safe rather than silently route to an unsupported endpoint and cause a 400.
- Preserve all semantically important signals through a translation: tool calls/tool_use blocks, reasoning content, finish_reason (including truncation reasons like `length`/`content_filter`), and usage data. Do not drop them just because the source/target shape differs (e.g. a Responses→Chat-Completions converter must not report `tool_calls` as the finish reason when output was truncated and the call is incomplete; a provider executor's stream parser must pass through `tool_calls`/`tool_use` deltas, not just plain text, or multi-turn agent workflows break).
- Guard terminal/one-shot events (content_block_stop, message_delta, message_stop, finish reason) with idempotency flags (e.g. `closed`, `finishReasonSent`, `messageStopSent`) so a later chunk carrying extra data (like final usage) can still be forwarded without re-emitting already-closed blocks or duplicating terminal markers.
- Apply any cross-cutting interception/rewrite logic (e.g. web_search redirection) at every exit point where a response can reach the client — native passthrough, converted chat/gemini bodies, and SSE-to-JSON conversions — not just the first handler you touch, and keep the logic internally guarded so it's a no-op when not applicable.
- Add a regression test per edge case (truncation, duplicate finish chunks, missing tool_calls, each client format) so the translation surface doesn't silently regress as new providers/models are added.

Example pattern for idempotent terminal emission:
```js
if (!state.finishReasonSent) {
  state.finishReasonSent = true;
  state.finishReason = choice.finish_reason;
}
// later, a usage-only finish chunk should still be forwarded
if (!state.messageStopSent) { /* emit message_stop once */ }
```