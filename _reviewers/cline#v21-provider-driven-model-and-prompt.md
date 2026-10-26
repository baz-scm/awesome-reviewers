---
title: Provider-driven model and prompt
description: When wiring AI/LLM behavior (model selection, system prompts, request
  shaping), base decisions on provider/model metadata and capability-aware logic—avoid
  hardcoded fallbacks and fragile local workarounds.
repository: cline/cline#v21
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70886
---

When wiring AI/LLM behavior (model selection, system prompts, request shaping), base decisions on provider/model metadata and capability-aware logic—avoid hardcoded fallbacks and fragile local workarounds.

Apply:
- Model defaults: Prefer provider manifest fields (e.g., `defaultModelId`) and only fall back after handling placeholder/non-real catalog values; cover both paths with tests.
- System prompts: Use shared prompt builders/abstractions, keep prompts non-redundant, and make instruction changes depend on mode and explicit user intent.
- Adapter/request shaping: Ensure request fields are only sent when the model supports them; pin behavior with capability-aware tests.
- Avoid special handling: If the issue is in an upstream AI SDK adapter (e.g., sending unsupported Bedrock reasoning fields), fix upstream rather than duplicating fragile logic locally.
- Token limits: When implementing caps (max tokens, reasoning budgets), make “floor vs ceiling” semantics explicit in code/comments and preserve prior clamping behavior.

Example (model fallback pattern):
```ts
const defaultModel =
  (provider === "cline" || provider === "cline-pass")
    ? (await Llms.getProviderCollection(provider))?.provider?.defaultModelId
    : undefined;

const chosenModel =
  input.options.model?.trim() ||
  selectedProviderSettings?.model ||
  input.defaultModel ||
  defaultModel;
```
