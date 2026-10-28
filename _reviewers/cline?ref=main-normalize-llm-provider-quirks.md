---
title: Normalize LLM provider quirks
description: LLM providers (LM Studio, Bedrock, Vertex, OpenAI, Gemini, etc.) expose
  inconsistent, overlapping, or misleading fields for the same concept — context limits,
  reasoning-token accounting, model variants/ids, tool-schema shape, and streaming
  timeouts. Code that bridges these providers must pick the most accurate signal,
  normalize to one canonical shape, and...
repository: cline/cline?ref=main
label: AI
language: TypeScript
comments_count: 8
repository_stars: 70980
---

LLM providers (LM Studio, Bedrock, Vertex, OpenAI, Gemini, etc.) expose inconsistent, overlapping, or misleading fields for the same concept — context limits, reasoning-token accounting, model variants/ids, tool-schema shape, and streaming timeouts. Code that bridges these providers must pick the most accurate signal, normalize to one canonical shape, and be validated against every known provider variant rather than against a single happy path.

Concretely:
- When multiple fields can represent the same value, prefer the one that reflects the actual runtime limit over a nominal ceiling. E.g. for LM Studio, use `loaded_context_length` (what's actually served) instead of `max_context_length` (the model's theoretical ceiling), since falling back to the ceiling lets requests exceed what the server will actually accept before Cline's own compaction kicks in.
- Normalize heterogeneous response shapes into one internal representation instead of special-casing each provider inline. Usage normalization must check every known path a provider uses to report reasoning tokens (e.g. `completion_tokens_details.reasoning_tokens` vs. nested `outputTokens.reasoning`) and subtract them consistently so output-token counts, cost, and telemetry never double-book the same tokens. Add a regression test per shape you add support for.
- Don't apply one-size-fits-all defaults (timeouts, model ids, inference-profile patterns) without checking they hold across all supported configurations. A 2-minute `firstChunkMs` can be wrong for a reasoning model that thinks silently before streaming; a new `defaultModelId` can break API-key-only auth if the new model's adapter ignores the key; a regex for Bedrock inference-profile ids can miss region-specific prefixes (e.g. `in.` vs `apac.`). When in doubt, keep the known-safe default and scope the improvement narrower (e.g. only touch error messaging/metrics) rather than changing behavior broadly.
- Prefer fixing quirks upstream (e.g. in the AI SDK provider adapter) over scattering provider-specific workarounds through the codebase; if a local workaround is unavoidable, isolate it, document why, and note the upstream issue so it can be removed later.
- Any destructive or stateful operation keyed off provider metadata (e.g. deleting a model's files, unloading an instance) must verify the metadata unambiguously identifies the target — e.g. refuse to delete a model when multiple quantization variants share one model key, so a quantization the user didn't intend to remove is never touched.

Always add a test per newly supported provider shape/region/config so these fixes don't regress as more providers and defaults are added.