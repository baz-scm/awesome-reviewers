---
title: Accurate Parsing Estimation
description: When implementing algorithmic utilities (parsers, normalizers, token/complexity
  estimators), specify and enforce invariants, and test the edge cases that break
  naive implementations.
repository: cline/CLINE
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70839
---

When implementing algorithmic utilities (parsers, normalizers, token/complexity estimators), specify and enforce invariants, and test the edge cases that break naive implementations.

Practical rules:
- **Don’t estimate from the wrong signal.** For structured/opaque payloads (e.g., base64 images), use a model that matches how cost is counted (e.g., flat per-image cost), so irrelevant payload size doesn’t change the estimate.
- **Parse command output using the real delimiter contract.** If a field can contain delimiters (tabs, backslashes), split only where the format guarantees boundaries; keep the remainder intact.
- **Recursively handle nested structure.** If inputs can contain arrays/items and combinator branches, normalize/inspect them at every depth (and before applying object-like gates).
- **Add invariant-focused tests.** Include cases like tab-containing filenames, literal backslashes in path segments, and payload-size changes that should not affect results.

Example (estimator invariant: payload size shouldn’t move the estimate):
```ts
export const ESTIMATED_TOKENS_PER_IMAGE = 1_600;

export function estimateRequestInputTokens({ messages }: { messages: unknown[] }) {
  const base = estimateTokens(JSON.stringify({ messages } ).length);
  const imageCount = countImagesInMessages(messages); // implementation scans for {type:"image"}
  return base + imageCount * ESTIMATED_TOKENS_PER_IMAGE;
}
// Test invariant: increasing base64 length must not change the per-image delta.
```

If you can’t clearly state the invariant, you probably don’t have a robust algorithm yet—write one (what must stay unchanged, what must change) before coding, then lock it down with the edge-case tests.