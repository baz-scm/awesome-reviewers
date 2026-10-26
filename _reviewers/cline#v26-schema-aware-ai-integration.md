---
title: Schema Aware AI Integration
description: 'Ensure AI integration code treats provider/model behavior as a contract:
  centralize prompt/policy construction, be schema-precise about reasoning/token fields,
  avoid unnecessary provider-specific workarounds, and lock behavior with regression
  tests.'
repository: cline/cline#v26
label: AI
language: TypeScript
comments_count: 6
repository_stars: 70893
---

Ensure AI integration code treats provider/model behavior as a contract: centralize prompt/policy construction, be schema-precise about reasoning/token fields, avoid unnecessary provider-specific workarounds, and lock behavior with regression tests.

Apply this standard:
- Centralize prompt assembly using shared helpers; don’t manually concatenate ad-hoc rules.
  - Make behavior mode-aware (e.g., only encourage commit/push/PR when the mode implies changes).
- Treat usage and reasoning fields as exact schemas.
  - If reasoning tokens are reported inside nested fields (e.g., outputTokens.reasoning), subtract them so downstream “outputTokens” reflect only non-reasoning output.
  - For providers like Bedrock, only send reasoning fields that the target model supports; otherwise omit them entirely.
- Prefer upstream fixes over local special casing.
  - If an AI SDK adapter mis-emits fields for a provider, upstream the correction instead of adding brittle integration-specific patterns.
- Preserve token budgeting semantics.
  - When computing max output caps, keep intended “floor vs ceiling” behavior and ensure existing clamps remain in effect.
- Add regression tests that cover the exact problematic shapes/behaviors (nested usage fields, adapter translation for reasoning support, and token-cap semantics).

Example (prompt centralization + mode-gated policy):
```ts
import { buildClineSystemPrompt } from "@cline/shared";

const shouldSuggestPR = mode === "act" || mode === "yolo";
const PR_INSTRUCTIONS = shouldSuggestPR
  ? "When work is complete, offer to commit, push, and open a PR ..."
  : "";

const systemPrompt = buildClineSystemPrompt({
  ide: "Cloud Agent",
  cwd,
  workspaceName: basename(cwd),
  rules: `${CLOUD_SESSION_SYSTEM_PROMPT}\n${PR_INSTRUCTIONS}`,
  mode,
  providerId: "cline",
  platform: "Linux",
});
```

Example (usage schema correctness: subtract nested reasoning from outputTokens):
```ts
outputTokens = Math.max(0, normalizedUsage.outputTokens - reasoningTokenCount);
// reasoningTokenCount should include nested paths like outputTokens.reasoning when present.
```