---
title: Provider Metadata Mapping
description: When integrating with multiple model providers, treat provider-reported
  capabilities (context length, token limits, reasoning support, default models) as
  *schema-variant and capability-gated*. Implement a single, precedence-based mapping
  layer and avoid sending “best guess” fields that providers reject.
repository: cline/cline#v22
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70886
---

When integrating with multiple model providers, treat provider-reported capabilities (context length, token limits, reasoning support, default models) as *schema-variant and capability-gated*. Implement a single, precedence-based mapping layer and avoid sending “best guess” fields that providers reject.

Apply these rules:
- **Map context/token limits using provider-specific keys** with an explicit precedence order.
  - Example precedence from observed providers:
    - **LM Studio**: prefer `loaded_context_length` (served capacity) over `max_context_length` (ceiling).
    - **vLLM**: use `max_model_len` instead of falling back to a generic default.
- **Avoid hardcoded cross-provider default models.**
  - Prefer `provider manifest defaultModelId`.
  - If a local provider uses a catalog-less placeholder like `"default"`, skip it and then fall back to a known project default.
- **Gate provider-specific request fields (e.g., Bedrock reasoning) by classification.**
  - If the system cannot confidently classify the model’s reasoning support, **send no reasoning fields** rather than sending an incompatible structure.
- **Minimize scattered special-casing.**
  - If the bug is in an adapter’s translation (e.g., it “accidentally sends reasoning”), prefer an upstream/adapter fix over adding custom routing logic.

Code sketch (precedence mapping):
```ts
type RawEntry = Record<string, unknown>;

function positiveInt(v: unknown): number | undefined {
  return typeof v === 'number' && Number.isFinite(v) && v > 0 ? Math.trunc(v) : undefined;
}

function toContextWindow(entry: RawEntry): number | undefined {
  // LM Studio: served vs ceiling
  const loaded = positiveInt(entry['loaded_context_length']);
  if (loaded) return loaded;

  // Common/ceiling-like fields
  const max = positiveInt(entry['max_context_length']) ?? positiveInt(entry['context_window']);
  if (max) return max;

  // vLLM
  return positiveInt(entry['max_model_len']);
}
```

Outcome: fewer incorrect fallbacks (e.g., 128K), fewer premature rejections (e.g., compaction too late), and safer provider requests (no unsupported reasoning fields).