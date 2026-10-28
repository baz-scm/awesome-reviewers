---
title: Normalize provider quirks
description: 'When integrating with multiple LLM providers and models, code must account
  for the full, real-world range of API variations rather than the one or two cases
  that happened to be tested. Providers and model families diverge in subtle ways:
  field names for the same concept (context window reported as `context_length`, `context_window`,
  vLLM''s `max_model_len`,...'
repository: cline/cline#|sleep 4
label: AI
language: TypeScript
comments_count: 7
repository_stars: 70979
---

When integrating with multiple LLM providers and models, code must account for the full, real-world range of API variations rather than the one or two cases that happened to be tested. Providers and model families diverge in subtle ways: field names for the same concept (context window reported as `context_length`, `context_window`, vLLM's `max_model_len`, or LM Studio's `max_context_length` vs. the actually-loaded `loaded_context_length`), auth mechanisms (plain API key/baseUrl vs. IAM roles, instance profiles, default credential chains, or OAuth), tool-schema encoding (uppercase JSON-schema types, `null` sent for unused or unsupported fields, nested `items`/`anyOf`/`oneOf`/`allOf` branches), and reasoning/thinking configuration per model family. When writing a normalizer or resolver for this kind of input, enumerate every known provider-specific shape (not just the first one you hit), and prefer reusing an existing, well-exercised capability/usability check (e.g., the same "is this provider usable" logic the UI already uses) over a narrow, ad hoc presence check that silently rejects valid configurations such as Bedrock profiles or Vertex GCP credentials.

Avoid baking specific model names into logic or comments to explain a workaround — model line-ups change constantly and the comment rots or becomes mis-attributed. Describe the actual protocol/schema behavior instead, e.g.:

```ts
// Advertise old_text as a plain string: when the schema allows null, some
// models send null instead of the real text for replacement edits. Other
// models send null for optionals they aren't using, so null is still
// accepted at runtime and treated as omitted.
```

Finally, before building a custom compatibility/routing layer for a provider, check whether the underlying SDK already does the right translation (e.g., Bedrock's `reasoning` top-level option is translated per model family by `@ai-sdk/amazon-bedrock` itself) — a thin pass-through is both less code and less likely to drift from upstream behavior than a hand-rolled equivalent.