---
title: AI Provider Integration Robustness
description: When integrating with LLM/vision providers, keep core logic aligned with
  provider semantics (billing/validation) and avoid brittle provider-specific workarounds.
repository: cline/cline#v13
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70874
---

When integrating with LLM/vision providers, keep core logic aligned with provider semantics (billing/validation) and avoid brittle provider-specific workarounds.

Apply these rules:
1) Use model-accurate accounting/sanitization for token budgeting
- If an estimator relies on message size (chars/bytes), sanitize or normalize payloads that are billed differently (e.g., base64 image data). Add an explicit, flat cost for image blocks instead of letting base64 length inflate token estimates.

```ts
export const ESTIMATED_TOKENS_PER_IMAGE = 1_600;

export function createImageAwareReplacer(): {
  replacer: (key: string, value: unknown) => unknown;
  imageCount: () => number;
} {
  let count = 0;
  const replacer = (_key: string, value: unknown): unknown => {
    if (!value || typeof value !== "object") return value;
    const t = (value as { type?: unknown }).type;
    if (t !== "image") return value;
    const record = value as Record<string, unknown>;
    if (typeof record.data === "string") { count += 1; return { ...record, data: "" }; }
    if ("image" in record) { count += 1; return { ...record, image: "" }; }
    return value;
  };
  return { replacer, imageCount: () => count };
}
```

2) Parse provider catalog metadata with provider-specific field names
- Don’t assume the same key names across providers. If a provider reports context/window under a different field, map it explicitly (e.g., vLLM’s `max_model_len`). This prevents silent fallbacks to incorrect defaults.

3) Don’t duplicate adapter bugs as local special handling
- If the wrong payload shape is sent (e.g., reasoning fields for models that don’t support them), prefer fixing/upstreaming the adapter/routing layer rather than introducing “special pattern” logic in the core.
- Where local logic must exist temporarily, keep it bounded, justified, and documented with the exact contract it enforces (what gets sent/omitted and why).

Outcome: fewer invalid provider requests, more accurate cost control, and less brittle code spread across the codebase.