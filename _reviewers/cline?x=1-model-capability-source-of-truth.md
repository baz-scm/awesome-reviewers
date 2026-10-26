---
title: Model capability source-of-truth
description: When building requests for LLM providers, always treat advertised model
  capabilities (catalog/model-list fields and provider manifests) as the source of
  truth, and make fallbacks explicit.
repository: cline/cline?x=1
label: AI
language: TypeScript
comments_count: 4
repository_stars: 70861
---

When building requests for LLM providers, always treat advertised model capabilities (catalog/model-list fields and provider manifests) as the source of truth, and make fallbacks explicit.

Practical rules:
1. Do not hardcode a global “last resort” model in request-building paths. Prefer provider-specific `defaultModelId` and handle known placeholders (e.g., catalog-less/local “default” entries) before falling back.
2. Parse provider model-list entries into a structured model descriptor (id + optional capability fields like context window / max tokens). Preserve provider-specific field names (e.g., vLLM’s `max_model_len`) so you don’t silently fall back to an unrelated constant.
3. Keep provider-translation logic (e.g., Bedrock reasoning-field mapping) in the adapter layer, not scattered through routing/resolvers. If the adapter is wrong, fix it where the translation happens (and upstream if appropriate), and keep resolver tests focused on the boundaries it owns.
4. For token budgeting defaults, document and implement clear semantics (e.g., “flat default is a floor; fraction may raise it; later clamps enforce model/context reality”), and ensure tests cover these regressions.

Example (pattern for capability-aware defaults):
```ts
export interface ModelSourceEntry {
  id: string;
  contextWindow?: number;
  maxOutputTokens?: number;
}

function toModelSourceEntry(item: unknown): ModelSourceEntry | undefined {
  if (typeof item === "string") {
    const id = item.trim();
    return id ? { id } : undefined;
  }
  const entry = (item && typeof item === "object" && !Array.isArray(item)) ? (item as any) : undefined;
  if (!entry) return undefined;

  const id = (entry.id ?? entry.name ?? entry.model);
  if (typeof id !== "string" || !id.trim()) return undefined;

  // Preserve provider-specific capability fields.
  const maxOutputTokens =
    typeof entry.max_model_len === "number" ? entry.max_model_len : entry.maxOutputTokens;

  return {
    id: id.trim(),
    contextWindow: entry.context_length,
    maxOutputTokens,
  };
}

function resolveMaxOutputTokens({
  defaultMaxOutputTokens,
  modelMaxOutputTokens,
  flatDefault,
  fraction,
}: {
  defaultMaxOutputTokens?: number;
  modelMaxOutputTokens?: number;
  flatDefault: number;
  fraction: number;
}) {
  // flatDefault is a floor; fraction may raise, then later clamps will enforce reality.
  const base = defaultMaxOutputTokens ?? flatDefault;
  if (defaultMaxOutputTokens !== undefined || typeof modelMaxOutputTokens !== "number") return base;
  return Math.max(base, Math.floor(modelMaxOutputTokens * fraction));
}
```