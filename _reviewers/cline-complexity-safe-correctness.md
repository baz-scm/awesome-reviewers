---
title: Complexity-Safe Correctness
description: When implementing algorithmic logic (parsing, path transforms, selection/slicing,
  or cost/estimate functions), treat correctness and runtime bounds as first-class
  requirements.
repository: CLINE/CLINE
label: Algorithms
language: TypeScript
comments_count: 6
repository_stars: 70837
---

When implementing algorithmic logic (parsing, path transforms, selection/slicing, or cost/estimate functions), treat correctness and runtime bounds as first-class requirements.

Apply this standard:
1) State the invariant explicitly
- Define what gets counted and when (e.g., “only after the newest real prompt” vs. earlier turns).
- Define precedence rules (e.g., `disabled` overrides `enabled: false`).
- Define structural boundaries (e.g., how many lines a top-level YAML entry spans so inline comments attach correctly).
- Define path semantics (e.g., POSIX conversion must not change filenames that legitimately contain backslashes).

2) Avoid naive scaling/assumptions; cap complexity/cost
- For estimators, make the function depend on the intended drivers (e.g., image count) rather than incidental payload size.
- For potentially large inputs/archives, enforce explicit size limits and bounded recursion/depth.
- Avoid pathological regex patterns that can cause backtracking blowups.

3) Add targeted tests that break naive implementations
- Estimation: verify independence from large payload size and correct scaling with count.
- Parsing: verify precedence and boundary inclusion (block scalars, comments, re-enabling).
- Transforms: verify edge-case filenames (literal backslashes).
- Selection/slicing: verify earlier-state cannot affect later verification.

Example pattern (estimation should be count-based, not payload-based):
```ts
const ESTIMATED_TOKENS_PER_IMAGE = 123;

function estimateTokensForImages(content: Array<{type: string; data?: string}>) {
  const imageCount = content.filter(b => b.type === 'image').length;
  return imageCount * ESTIMATED_TOKENS_PER_IMAGE;
}
```
Back it with tests that compare a huge base64 payload vs. a small one (same count → same estimate) and verify the estimate scales ~linearly with image count.

This combination prevents both subtle semantic bugs and worst-case performance surprises in the algorithmic parts of the system.