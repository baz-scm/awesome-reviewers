---
title: Model-aware limits and reasoning
description: When building AI/gateway/provider request logic, derive token budgets
  and reasoning payloads from the most accurate, provider-verified model metadata,
  and make defaulting/clamping semantics explicit.
repository: cline/CLINE
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70839
---

When building AI/gateway/provider request logic, derive token budgets and reasoning payloads from the most accurate, provider-verified model metadata, and make defaulting/clamping semantics explicit.

Practical rules:
1) Prefer “effective” limits from the catalog/provider
- If the provider exposes both a ceiling and a served/loaded value, use the served/loaded value for budgeting so downstream logic doesn’t overestimate capacity.

2) Emit reasoning fields only when you can prove the provider/model supports them
- Don’t send generic reasoning payloads “just because” an id name doesn’t match a known family.
- Tests should pin these translation boundaries (supported family → send the provider-accepted field; unclassified/unsupported → send none; preserved id-derived native shapes when the catalog lags).

3) Encode defaults as floors/ceilings with documentation, then clamp
- If a numeric default is intended as a floor, document that it may be raised proportionally only under safe conditions, and rely on later model/context clamps to enforce hard ceilings.

4) Avoid accumulating duplicated provider special-cases
- If the correct fix belongs in the underlying adapter/library, upstream it; don’t scatter one-off “bedrock-like” handling across your codebase.

Example pattern (budget + safe reasoning emission):
```ts
function resolveMaxOutputTokens({ model, input, reasoningFloor }: {
  model: { maxOutputTokens?: number };
  input: { defaultMaxOutputTokens?: number };
  reasoningFloor: number;
}) {
  const baseDefault = input.defaultMaxOutputTokens ?? DEFAULT_GATEWAY_MAX_OUTPUT_TOKENS;
  // baseDefault is a floor; only raise it proportionally when safe.
  const baseWithCatalogRaise =
    input.defaultMaxOutputTokens === undefined &&
    isPositiveFiniteNumber(model.maxOutputTokens)
      ? Math.max(
          baseDefault,
          Math.floor(model.maxOutputTokens * DEFAULT_GATEWAY_MAX_OUTPUT_FRACTION),
        )
      : baseDefault;

  const withReasoning = baseWithCatalogRaise + reasoningFloor;
  return clampToModelAndContext(withReasoning, model);
}

function buildProviderReasoningPayload({
  modelFamily,
  isSupportedInferenceProfile,
}: {
  modelFamily: string;
  isSupportedInferenceProfile: boolean;
}) {
  if (isSupportedInferenceProfile) {
    // send only the provider-accepted reasoning field
    return { reasoning: { effort: /* ... */ } };
  }
  // If unclassified/unsupported, send none (avoid rejected generic fields)
  return {};
}
```

Mode-aware addendum (agent behavior): vary “do commit/PR” prompts by the user’s execution mode—don’t apply commit/PR side effects in Plan-like modes unless explicitly requested by the user.