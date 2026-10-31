---
title: Centralize model-specific logic
description: Avoid hardcoding model IDs, provider formats, or model-family checks
  directly in business logic; this creates duplicated knowledge that drifts out of
  sync and breaks when new models or providers are added. Prefer a centralized model
  registry or typed provider enum as the single source of truth for model IDs, response
  formats, and usage/pricing structures,...
repository: Helicone/helicone
label: AI
language: TypeScript
comments_count: 5
repository_stars: 6248
---

Avoid hardcoding model IDs, provider formats, or model-family checks directly in business logic; this creates duplicated knowledge that drifts out of sync and breaks when new models or providers are added. Prefer a centralized model registry or typed provider enum as the single source of truth for model IDs, response formats, and usage/pricing structures, and design shared types (e.g., usage tracking) to mirror the actual provider API shape rather than inventing a custom flattened structure.

When full abstraction isn't yet feasible, make hardcoded checks resilient and self-documenting:
- Use pattern matching instead of exact-match lists for model families that will grow (e.g., match `o[1-9]+(-mini)?` instead of `["o1", "o3-mini"].includes(model)`).
- Type provider/format parameters explicitly instead of accepting raw strings, and fail loudly (throw) for unsupported providers rather than silently defaulting.
- If you must temporarily hardcode provider-specific mappings (e.g., Claude model aliases), file a follow-up ticket to migrate the logic into the registry, and verify the change doesn't silently alter behavior for existing consumers (e.g., confirm `NO_MAPPING` still resolves to the correct format for all current integrations).

Example of a more robust guard instead of an exact-match list:
```ts
// Fragile: breaks silently once o4, o5, ... are released
if (["o1", "o3-mini"].includes(model)) { ... }

// Better: generalizes across the model family
if (/^o[1-9]+(-mini)?$/.test(model)) { ... }
```