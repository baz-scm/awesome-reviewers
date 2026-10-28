---
title: Model capability routing
description: LLM providers and models vary in context limits, reasoning support, tool-schema
  requirements, and streaming timing — never hardcode a single assumption across all
  of them. Derive routing decisions from the capability data you actually have (a
  model catalog, a provider's live model-list response, or the specific family an
  id belongs to) instead of a blanket...
repository: cline/cline#&&sleep 4
label: AI
language: TypeScript
comments_count: 9
repository_stars: 70980
---

LLM providers and models vary in context limits, reasoning support, tool-schema requirements, and streaming timing — never hardcode a single assumption across all of them. Derive routing decisions from the capability data you actually have (a model catalog, a provider's live model-list response, or the specific family an id belongs to) instead of a blanket heuristic:

- Context/token budgets: when a provider reports both a ceiling and the amount actually being served (e.g. LM Studio's `max_context_length` vs `loaded_context_length`), use the served value for compaction/truncation budgets, not the ceiling — otherwise the budget undercounts and the provider rejects requests before compaction kicks in.
- Reasoning/thinking options: only forward a provider-specific reasoning field (e.g. Bedrock's `reasoningConfig`) when the catalog confirms the target model advertises that control; gate this through a required context parameter so a call site can't silently skip the check. Prefer simplifying by model family (e.g. "is this Anthropic vs OpenAI on Bedrock") over ad-hoc per-id special-casing, and consider whether the fix belongs upstream in the SDK/adapter rather than as a local workaround.
- Timeouts: a "first chunk" timeout must account for how the model actually streams — a high-effort reasoning model can legitimately produce no text/reasoning delta for minutes, so a short first-chunk timeout will abort healthy requests. Size timeouts (or make them opt-in) based on observed model behavior, not an arbitrary short default.
- Tool-call/JSON schemas sent to models: normalize recursively (through `items`, `anyOf`/`oneOf`/`allOf`, nested `properties`) and match what each provider actually requires (e.g. Gemini needs tool parameters to resolve to `{ type: "object" }` even for a bare/scalar root schema).
- Provider identification (e.g. Azure vs DeepSeek vs base OpenAI-compatible) should be a single, explicit condition — don't duplicate or fork the detection logic for a special case; extend the existing check.

Back every one of these behaviors with a wire-contract test that exercises the real adapter/provider (not a mock of it), asserting on the literal request shape sent over the wire for each capability branch (recognized id, unlisted id, family-specific shape). This catches silent regressions when an upstream SDK or provider catalog changes behavior, and keeps the test's claims narrow enough to match exactly what is and isn't exercised (e.g. don't claim "no assertion depends on the catalog" if a resolver still consults it for ID rewriting).