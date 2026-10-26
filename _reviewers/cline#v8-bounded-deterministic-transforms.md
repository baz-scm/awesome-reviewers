---
title: Bounded, deterministic transforms
description: 'When implementing algorithms for transformation/normalization/estimation,
  require two properties: (1) deterministic, stable outputs under the same logical
  inputs, and (2) bounded worst-case work that cannot be driven by adversarial payload
  size or pathological syntax.'
repository: cline/cline#v8
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 70867
---

When implementing algorithms for transformation/normalization/estimation, require two properties: (1) deterministic, stable outputs under the same logical inputs, and (2) bounded worst-case work that cannot be driven by adversarial payload size or pathological syntax.

Apply this standard:
- Clamp/normalize *before* hashing/ID generation so ids don’t drift when text exceeds published limits.
  - Example pattern:
    ```ts
    const clip = (s: string, max: number) => s.slice(0, max);
    const stableId = (kind: string, prompt: string) => fnv1a32(`${kind}:${clip(prompt, PROMPT_MAX)}`);
    ```
- Normalize recursively through all relevant structural branches before applying object-vs-non-object gates (e.g., `items`, `anyOf`/`oneOf`/`allOf`, nested schemas).
- Prevent naive cost models: token/image estimators must be based on the real cost driver (e.g., count images; don’t charge base64 length as chars).
- Bound computational work:
  - avoid regexes known to backtrack badly on long inputs; prefer linear scans/loops;
  - cap recursion/expansion depth (e.g., symlink/link expansion); cap downloaded/archive sizes and total copied bytes.
- Prove correctness with tests suited to algorithms:
  - use fixtures for invariants (e.g., checkpoint/state history) and
  - add property/fuzz tests for state-machine transitions (e.g., ordered pagination with “skip”/undo).