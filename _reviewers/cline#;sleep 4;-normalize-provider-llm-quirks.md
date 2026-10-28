---
title: Normalize provider LLM quirks
description: 'LLM providers and local-server adapters (OpenAI, Anthropic, Bedrock,
  vLLM, LM Studio, etc.) each expose context limits, token-usage breakdowns, streaming/timeout
  behavior, and tool-schema shapes differently. Never assume one provider''s shape,
  default, or timing behavior generalizes to all others — explicitly map and test
  each quirk:'
repository: cline/cline#;sleep 4;
label: AI
language: TypeScript
comments_count: 11
repository_stars: 70976
---

LLM providers and local-server adapters (OpenAI, Anthropic, Bedrock, vLLM, LM Studio, etc.) each expose context limits, token-usage breakdowns, streaming/timeout behavior, and tool-schema shapes differently. Never assume one provider's shape, default, or timing behavior generalizes to all others — explicitly map and test each quirk:

- Context/token limits: read every field name a catalog may use (OpenAI `context_length`, vLLM `max_model_len`, LM Studio `max_context_length` vs. the currently-loaded `loaded_context_length`), and prefer the safest/currently-effective value rather than the advertised max, so budgets such as compaction don't let the server start rejecting requests.
- Usage accounting: reasoning/thinking tokens are nested under different keys per provider/SDK version (e.g. `completion_tokens_details.reasoning_tokens` vs. `outputTokens.reasoning`). Normalize every known shape and add a regression test per shape so tokens are neither double-counted nor silently dropped.
- Streaming timeouts and retries: timers and retry logic must reflect real model behavior (e.g. reasoning models can go minutes without emitting a chunk) and must only retry when the SDK marks the error retryable, with backoff, never blindly replaying a request after provider-executed tool side effects have already occurred.
- Reasoning/tool-schema routing: provider-specific adapter gates (e.g. Bedrock vs. Anthropic reasoning translation, Gemini's strict `type: object` schema requirement) must be driven by explicit, required context passed to the resolver — not by hoping an earlier short-circuit always runs — and schema normalization must recurse into every nested structure (`items`, `anyOf`/`oneOf`/`allOf`) rather than only the top level.

When adding support for a new provider or SDK version, isolate the quirk in a small, well-documented adapter function (cite the vendor doc or tracking issue), and cover it with a dedicated test so the specific shape can't regress silently.
