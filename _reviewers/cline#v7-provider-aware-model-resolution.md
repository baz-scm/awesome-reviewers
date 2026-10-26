---
title: Provider-aware model resolution
description: When resolving model IDs and generating provider-specific request parameters,
  derive capabilities from the provider’s own manifests/catalog and emit only fields
  the provider can accept.
repository: cline/cline#v7
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70865
---

When resolving model IDs and generating provider-specific request parameters, derive capabilities from the provider’s own manifests/catalog and emit only fields the provider can accept.

Actionable rules:
- Don’t drop vendor-specific capability fields from model lists. If a provider reports context/window under different keys (e.g., vLLM `max_model_len`), extend your parser to read them so you don’t silently fall back to a generic default.
- Don’t hardcode a single “last resort” model across providers. Prefer the provider manifest’s `defaultModelId` when it’s a real model; skip placeholder values exposed by catalog-less/local providers; then fall back to your global constant only if necessary.
- Provider request shaping must be capability-correct:
  - If a provider accepts reasoning controls only for certain model families, send the provider’s accepted field shape (e.g., Bedrock `reasoning.effort`) only for supported models.
  - For models you cannot classify as reasoning-capable, send no reasoning fields at all (don’t guess with a generic field like `reasoningConfig`).
  - Preserve native request-field shapes for classified families even if the catalog lags.
- Defaulting logic must respect semantic intent (e.g., treat your “flat” output cap as a floor, not a ceiling, and only raise it via fractions for sufficiently large advertised budgets; then clamp using the model/context limits).
- Avoid scattering adapter-specific special cases in multiple places. If the incorrect behavior is in an SDK adapter’s translation, fix it upstream to the adapter layer.

Example (pattern for provider-safe defaulting):
```ts
const modelId =
  (selectedProviderSettings?.model ?? input.options.model?.trim()) ||
  (providerHasManifestDefault
    ? manifest.defaultModelId
    : undefined) ||
  // Skip placeholder "default" (catalog-less/local providers)
  (manifest.defaultModelId && manifest.defaultModelId !== "default"
    ? manifest.defaultModelId
    : undefined) ||
  CLINE_DEFAULT_MODEL_ID;
```
Example (pattern for provider-safe reasoning fields):
```ts
const reasoningFields = isReasoningSupported(modelId)
  ? { reasoning: { effort: effortValue } } // provider-accepted shape
  : {}; // otherwise emit nothing
```