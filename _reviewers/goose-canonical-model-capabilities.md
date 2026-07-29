---
title: Canonical Model Capabilities
description: When integrating LLM providers/models, derive capability flags and limits
  from canonical model metadata (catalog) and apply deterministic compatibility rules
  with explicit fallbacks—avoid brittle name-based heuristics and keep user overrides
  authoritative.
repository: aaif-goose/goose
label: AI
language: Rust
comments_count: 8
repository_stars: 51876
---

When integrating LLM providers/models, derive capability flags and limits from canonical model metadata (catalog) and apply deterministic compatibility rules with explicit fallbacks—avoid brittle name-based heuristics and keep user overrides authoritative.

Apply these practices:
- Canonical-first: use canonical model data for flags like thinking/reasoning/temperature support instead of substring checks on model names.
- Separate decisions: keep helpers for distinct behaviors (e.g., “omit temperature” vs “allow reasoning_effort”) and add allowlists/exclusions with payload/unit tests.
- Respect overrides: when resolving `context_limit`/`max_tokens` from a catalog, override only when the user/config limit is unset or the documented sentinel; cap `max_tokens` to the effective context (user override wins).
- Provider-safe fallbacks: in message/tool formatting, preserve critical fields (e.g., thinking/reasoning blocks) by using intentional fallbacks across intermediate chunks where OpenAI-compatible providers can drop state.
- Parity in accounting/serialization: normalize provider-specific fields (e.g., fold “thought” tokens into `output_tokens` where needed) so downstream logic and cost accounting remain consistent.

Example pattern (resolve limits with canonical fallback while honoring user overrides):
```rust
pub fn with_catalog_provider_fallback(mut self, catalog_provider_id: &str) -> Self {
    let canonical = maybe_get_canonical_model(catalog_provider_id, &self.model_name);
    if let Some(c) = canonical {
        // only override when user didn’t set a real limit
        if self.context_limit.is_none() || self.context_limit == Some(0) {
            self.context_limit = Some(c.limit.context);
        }
        // cap to effective context (not the raw catalog context)
        if self.max_tokens.is_none() {
            let effective_ctx = self.context_limit.unwrap_or(c.limit.context);
            self.max_tokens = c.limit.output
                .filter(|&out| out < effective_ctx)
                .map(|out| out as i32);
        }
    }
    self
}
```