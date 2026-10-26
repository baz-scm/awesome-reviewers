---
title: AI Semantics Consistency
description: When working on LLM/AI integrations, make AI behavior semantically correct
  and consistent across model choice, prompting, reasoning fields, and token accounting—then
  lock it in with regression tests.
repository: cline/cline#v16
label: AI
language: TypeScript
comments_count: 7
repository_stars: 70882
---

When working on LLM/AI integrations, make AI behavior semantically correct and consistent across model choice, prompting, reasoning fields, and token accounting—then lock it in with regression tests.

Apply this standard:
1) Prefer authoritative defaults + safe fallbacks
- Select default models from provider/manifest metadata (e.g., `defaultModelId`) rather than hardcoded ids.
- Handle “placeholder”/non-real catalog entries explicitly.

2) Build prompts centrally and make instructions mode-aware
- Assemble system prompts via shared helpers so format stays consistent.
- Adjust behavioral instructions (e.g., commit/PR expectations) based on agent mode and user intent.

3) Normalize reasoning and usage so outputs aren’t double-counted
- Ensure `outputTokens` represents non-reasoning output only.
- Subtract reasoning tokens from all relevant usage shapes (including nested fields).

4) Treat provider quirks as correctness bugs, not ad-hoc patches
- If the adapter/library sends unsupported reasoning fields, prefer fixing upstream (or in the shared adapter layer) rather than adding bedrock/provider-specific branching everywhere.
- Still add targeted tests for the translation/shape paths you depend on.

5) Compute limits with intentional floors and clamp to model budgets
- Token caps should use clear “floor vs ceiling” logic and preserve existing truncation/retry characteristics, then clamp to model/context budgets.

Minimal example (prompt + usage normalization patterns):
```ts
// 1) Mode-aware system prompt assembly (centralized helper)
const systemPrompt = buildClineSystemPrompt({
  ide: "Cloud Agent",
  cwd,
  workspaceName: basename(cwd),
  rules: CLOUD_SESSION_SYSTEM_PROMPT +
    (mode === "plan" ? "" : "\n\nWhen work is complete, offer commit/push/PR..."),
  mode,
  providerId: "cline",
  platform: "Linux",
});

// 2) Truthful token accounting (reasoning removed from outputTokens)
const reasoningTokenCount = getReasoningTokens(normalizedUsage); // includes nested paths
return {
  ...normalizedUsage,
  outputTokens: Math.max(0, normalizedUsage.outputTokens - reasoningTokenCount),
};
```

If you’re tempted to add a provider-specific special case, stop and ask: “Can we normalize this in the shared adapter/gateway layer (or upstream) so the rest of the codebase stays provider-agnostic?”