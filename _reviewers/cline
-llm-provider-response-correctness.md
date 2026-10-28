---
title: LLM provider response correctness
description: When integrating LLM provider SDKs (AI SDK, Bedrock, OpenAI, etc.), never
  trust the abstraction's defaults for token accounting, reasoning content, or schema
  shape — verify against the provider's actual wire behavior and pin regression tests
  to it.
repository: 'cline/cline

  '
label: AI
language: TypeScript
comments_count: 11
repository_stars: 70942
---

When integrating LLM provider SDKs (AI SDK, Bedrock, OpenAI, etc.), never trust the abstraction's defaults for token accounting, reasoning content, or schema shape — verify against the provider's actual wire behavior and pin regression tests to it.

Key practices:
- Token usage: reasoning tokens are typically a subset of outputTokens (e.g. OpenAI's `completion_tokens_details.reasoning_tokens`), not additional to it. Normalize usage so `outputTokens` reflects true non-reasoning output while tracking `reasoningTokenCount` separately, and account for every known nested shape providers may emit (e.g. `outputTokens.reasoning` for older SDK versions), each covered by a dedicated regression test with real response shapes.
- Tool/schema normalization: when massaging tool input schemas for provider compatibility (e.g. lowercasing `type`, defaulting a bare/scalar schema to `{ type: "object" }` for providers like Gemini), recurse into every nested location a schema can appear — `properties`, `items` (array and tuple forms), and `anyOf`/`oneOf`/`allOf` branches — not just the top level.
- Provider quirks: before adding provider-specific special-casing (e.g. a Bedrock-only reasoning router), check whether the quirk is really provider-specific or shared across model families routed through that provider (Bedrock Anthropic vs OpenAI use the same `providerOptions` shape as their native SDKs), and prefer fixing it upstream in the adapter when the bug is in the adapter itself.
- Completion/finish-reason handling: a `stop` finish with reasoning-only content (no text, tool call, media, or provider-executed tool activity) is not a real completion and should be treated like `unknown` so the run continues; don't let a model "finish" on an invisible reasoning block.
- Retry/recovery flows (e.g. max-tokens compaction retry): never discard content that already happened. If a retry produces completed provider-tool activity, reasoning, or tool calls before erroring or truncating again, that output must be preserved in conversation history, not silently dropped in favor of the original truncated turn — write table-driven tests across the full matrix of finish reasons × content types (text/tool-call/empty/provider-tool-activity) to prove nothing is lost.
- Timeouts: streaming timeouts (e.g. `firstChunkMs`/`chunkMs`) must account for providers/models that can go a long time between emitted deltas (long reasoning phases); don't apply an aggressive timeout as a default without confirming it won't abort valid high-effort responses.

Every provider-specific assumption like these should ship with a wire-level test exercised against the real adapter/version (not just a mock), since these behaviors change across SDK releases and silently regress otherwise.