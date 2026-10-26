---
title: AI Token Accounting Rules
description: Ensure all AI-related accounting (token estimation, usage normalization,
  and provider request translation) is correct under heterogeneous provider formats,
  and is conservative when uncertain.
repository: cline/cline#v27
label: AI
language: TypeScript
comments_count: 5
repository_stars: 70892
---

Ensure all AI-related accounting (token estimation, usage normalization, and provider request translation) is correct under heterogeneous provider formats, and is conservative when uncertain.

Apply these checks during code review:

1) Images: never bill base64 payload size char-by-char
- Estimation should follow the product’s semantics (typically flat per-image cost), so a single large base64 string doesn’t explode the token estimate.
- Add regression tests that compare against naive char-based math and ensure scaling is by image count, not encoded byte size.

2) Reasoning tokens: separate attribution from outputTokens
- If a provider reports reasoning tokens as a subset of `outputTokens` (including nested shapes like `outputTokens.reasoning`), subtract reasoning from `outputTokens` and track reasoning separately.
- Add tests covering both “reasoningTokenCount as its own field” and “reasoning nested under outputTokens”.

3) Capability fields in provider requests: only emit when supported
- When translating to provider-specific request schemas (e.g., Bedrock), only include reasoning-related fields if you can classify the model/family as supporting them.
- If classification fails, do not send reasoning fields the provider rejects.

4) Runtime limits: use “what is actually served”
- When reading model-list metadata, prefer fields representing the loaded/served context ceiling (e.g., `loaded_context_length` when present) over max ceilings that may not trigger compaction before rejections.

5) Prefer fixing at the right layer
- If the bug is caused by an adapter emitting the wrong request shape (e.g., reasoning fields), prefer an upstream adapter fix rather than proliferating local special-cases.

Minimal example of correct normalization for reasoning tokens:
```ts
function normalizeUsage({ outputTokens, reasoningTokenCount, outputTokensReasoning }: {
  outputTokens: number;
  reasoningTokenCount?: number;
  outputTokensReasoning?: number;
}) {
  const reasoning = reasoningTokenCount ?? outputTokensReasoning ?? 0;
  return {
    outputTokens: Math.max(0, outputTokens - reasoning),
    reasoningTokenCount: reasoning,
  };
}
```

If any of these are changing, require targeted regression tests that lock down the expected provider/model shapes (images, reasoning nested/subset formats, and conservative reasoning-field emission).