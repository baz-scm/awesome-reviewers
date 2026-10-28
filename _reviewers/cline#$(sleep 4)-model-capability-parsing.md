---
title: Model capability parsing
description: When reading model metadata (context window, token limits, reasoning
  support, etc.) from provider catalogs or APIs, do not assume a single field name
  or a uniform capability across providers and models. Provider catalogs expose limits
  under different keys (e.g. OpenAI's `context_length`, vLLM's `max_model_len`, LM
  Studio's `max_context_length`), so parsing...
repository: cline/cline#$(sleep 4)
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70978
---

When reading model metadata (context window, token limits, reasoning support, etc.) from provider catalogs or APIs, do not assume a single field name or a uniform capability across providers and models. Provider catalogs expose limits under different keys (e.g. OpenAI's `context_length`, vLLM's `max_model_len`, LM Studio's `max_context_length`), so parsing should check all known variants for a given provider rather than silently falling back to a generic default.

Also distinguish an advertised ceiling from the value actually enforced at serving time, and prefer the latter. For example, LM Studio reports both `max_context_length` (the model's theoretical ceiling) and, for a loaded instance, `loaded_context_length` (what it actually serves, which can be much smaller). If `maxInputTokens`/compaction budgets are derived from the ceiling instead of the serving value, compaction never triggers before the server starts rejecting requests. When both are available, prefer the more conservative/actual-serving value (or take the `min()` across reported limits) so the client fails safe rather than overruns the server's real limit.

The same caution applies to feature support, not just limits: before forwarding a provider-specific option (e.g. reasoning/thinking effort) to a model, verify via the model catalog or capability flags that the specific provider/model combination actually supports it. Blindly forwarding such options to unsupported models can cause hard API errors (e.g. "extra inputs are not permitted") instead of a graceful no-op.

In short: enumerate known field-name variants per provider, prefer actual-serving values over advertised maximums, and gate any provider-specific feature by verified per-model capability rather than assuming parity across providers.