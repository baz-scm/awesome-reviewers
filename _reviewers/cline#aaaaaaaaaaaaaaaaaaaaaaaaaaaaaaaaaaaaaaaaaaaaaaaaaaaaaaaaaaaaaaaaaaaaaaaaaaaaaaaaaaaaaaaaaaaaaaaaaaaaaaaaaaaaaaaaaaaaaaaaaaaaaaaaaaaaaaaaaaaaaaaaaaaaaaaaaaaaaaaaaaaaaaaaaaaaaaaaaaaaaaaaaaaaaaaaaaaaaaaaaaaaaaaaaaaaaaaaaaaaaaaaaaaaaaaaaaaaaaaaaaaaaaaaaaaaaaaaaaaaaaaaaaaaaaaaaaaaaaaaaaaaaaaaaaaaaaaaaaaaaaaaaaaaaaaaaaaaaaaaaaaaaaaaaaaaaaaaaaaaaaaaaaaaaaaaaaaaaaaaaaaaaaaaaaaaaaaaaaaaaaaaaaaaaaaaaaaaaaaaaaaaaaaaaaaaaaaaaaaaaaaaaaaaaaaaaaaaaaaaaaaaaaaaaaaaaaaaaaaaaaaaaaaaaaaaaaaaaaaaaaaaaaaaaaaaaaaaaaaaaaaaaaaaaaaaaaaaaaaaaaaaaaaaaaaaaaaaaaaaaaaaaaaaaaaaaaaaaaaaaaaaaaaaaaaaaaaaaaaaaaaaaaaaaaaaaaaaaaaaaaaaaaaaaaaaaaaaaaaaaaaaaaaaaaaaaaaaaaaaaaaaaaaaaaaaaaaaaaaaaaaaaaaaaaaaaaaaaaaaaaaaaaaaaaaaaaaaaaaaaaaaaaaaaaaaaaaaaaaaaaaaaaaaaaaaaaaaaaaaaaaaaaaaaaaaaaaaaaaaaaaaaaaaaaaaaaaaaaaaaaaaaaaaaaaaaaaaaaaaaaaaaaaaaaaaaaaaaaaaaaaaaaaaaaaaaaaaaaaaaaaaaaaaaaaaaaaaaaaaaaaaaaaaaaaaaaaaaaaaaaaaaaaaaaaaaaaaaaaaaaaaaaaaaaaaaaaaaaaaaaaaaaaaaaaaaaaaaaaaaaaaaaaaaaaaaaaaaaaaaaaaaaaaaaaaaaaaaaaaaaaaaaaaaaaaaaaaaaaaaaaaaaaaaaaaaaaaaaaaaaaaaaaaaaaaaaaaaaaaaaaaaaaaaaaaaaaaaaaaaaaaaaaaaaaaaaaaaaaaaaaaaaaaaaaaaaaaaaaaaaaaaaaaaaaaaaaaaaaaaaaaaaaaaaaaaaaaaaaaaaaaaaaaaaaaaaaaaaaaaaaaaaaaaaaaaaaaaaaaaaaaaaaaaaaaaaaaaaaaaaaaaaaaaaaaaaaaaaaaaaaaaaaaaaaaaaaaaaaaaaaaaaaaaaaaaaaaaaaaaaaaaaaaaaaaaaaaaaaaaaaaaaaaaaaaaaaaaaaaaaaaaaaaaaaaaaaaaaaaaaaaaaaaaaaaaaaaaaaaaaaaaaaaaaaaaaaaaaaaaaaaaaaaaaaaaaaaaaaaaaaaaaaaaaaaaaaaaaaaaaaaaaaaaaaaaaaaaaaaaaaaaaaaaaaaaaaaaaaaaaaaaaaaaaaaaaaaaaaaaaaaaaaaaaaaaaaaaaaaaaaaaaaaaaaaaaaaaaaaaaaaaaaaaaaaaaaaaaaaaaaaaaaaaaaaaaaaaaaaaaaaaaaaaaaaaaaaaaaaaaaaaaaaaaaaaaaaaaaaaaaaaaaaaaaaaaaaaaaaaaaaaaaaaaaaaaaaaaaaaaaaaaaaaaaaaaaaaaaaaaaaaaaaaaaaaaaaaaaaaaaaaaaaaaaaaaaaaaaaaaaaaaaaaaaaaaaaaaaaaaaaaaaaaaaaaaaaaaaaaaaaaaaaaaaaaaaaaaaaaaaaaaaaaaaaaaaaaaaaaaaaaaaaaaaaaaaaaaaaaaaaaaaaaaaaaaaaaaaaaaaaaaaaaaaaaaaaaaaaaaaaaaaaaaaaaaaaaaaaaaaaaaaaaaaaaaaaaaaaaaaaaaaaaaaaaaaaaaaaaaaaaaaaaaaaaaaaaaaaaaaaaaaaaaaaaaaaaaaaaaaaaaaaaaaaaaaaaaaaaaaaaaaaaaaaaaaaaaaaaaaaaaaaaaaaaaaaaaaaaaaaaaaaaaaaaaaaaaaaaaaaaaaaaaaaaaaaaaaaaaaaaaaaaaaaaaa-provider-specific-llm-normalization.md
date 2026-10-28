---
title: Provider-specific LLM normalization
description: 'LLM provider/model integrations (model catalogs, token usage, reasoning
  configs, tool schemas) are not uniform across vendors, and normalization code must
  be driven by each provider''s actual wire format rather than by an assumed common
  shape. Silently reusing one provider''s field name or config shape for another causes
  real regressions: falling back to a...'
repository: cline/cline#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70973
---

LLM provider/model integrations (model catalogs, token usage, reasoning configs, tool schemas) are not uniform across vendors, and normalization code must be driven by each provider's actual wire format rather than by an assumed common shape. Silently reusing one provider's field name or config shape for another causes real regressions: falling back to a wrong default context window when a provider uses a non-standard field name (e.g. vLLM's `max_model_len`, LM Studio's `loaded_context_length` vs `max_context_length`), rejecting requests when a reasoning field is sent to a model family that doesn't support it, or double-counting reasoning tokens when a provider nests them differently across SDK versions (e.g. `outputTokens.reasoning`).

When adding or updating provider normalization logic:
- Enumerate the known field variants per provider/vendor and map them explicitly (id, context window, max tokens, reasoning controls, etc.), documenting the source (API docs, catalog) for each field.
- Never assume a field name or shape generalizes across providers; verify against the provider's actual API/model-card documentation before adding a fallback.
- Gate provider-specific behavior (e.g. reasoning config forwarding) on a concrete capability check (does the catalog advertise this control for this model?) rather than on id pattern-matching alone, and avoid duplicating the same conditional logic in multiple branches — combine conditions where they share underlying logic.
- Add wire-level tests that exercise the real adapter/provider output (not just mocked constructors) so assertions pin the actual request/response shape sent to or received from the provider, and keep test/code comments precise about which parts are catalog-dependent versus fixed.
- For usage accounting, cover every known shape a provider or SDK version may use to report derived metrics (e.g. reasoning tokens as a top-level field vs nested under `outputTokens`) with explicit regression tests, so downstream consumers never double-count or silently drop data.

Example — mapping provider-specific context window fields explicitly rather than relying on a single assumed key:
```ts
const contextWindow = firstPositiveInteger(
  entry.context_length,       // OpenAI-compatible
  entry.context_window,
  entry.max_model_len,        // vLLM
  entry.loaded_context_length, // LM Studio: actual serving limit, prefer over max_context_length
  entry.max_context_length,   // LM Studio: static ceiling, fallback only
);
```
This keeps normalization honest about what each provider actually reports, and prevents mis-mapped defaults (like a 128K fallback) from masking a provider's real, smaller serving limit.