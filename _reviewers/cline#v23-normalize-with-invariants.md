---
title: Normalize With Invariants
description: For any non-trivial algorithm (state machine, parser, estimator, normalization,
  path handling), make the invariants explicit and enforce them through deterministic
  normalization. Then lock behavior down with targeted regression tests and, where
  feasible, property/fuzz tests. Also add complexity/robustness guards so irrelevant
  payload details don’t distort...
repository: cline/cline#v23
label: Algorithms
language: TypeScript
comments_count: 10
repository_stars: 70889
---

For any non-trivial algorithm (state machine, parser, estimator, normalization, path handling), make the invariants explicit and enforce them through deterministic normalization. Then lock behavior down with targeted regression tests and, where feasible, property/fuzz tests. Also add complexity/robustness guards so irrelevant payload details don’t distort results.

Apply these rules:
- **State invariants (paging/queues):** Define how cursor/pagination changes when actions occur (e.g., skip/remove). Ensure updates preserve “what’s visible” and “what’s pending” invariants.
- **Semantic preservation in parsers:** When parsing structured outputs (git status, YAML frontmatter, schema types), preserve required identity fields (e.g., rename/copy original path) and follow explicit precedence rules.
- **Deterministic normalization boundaries:** Normalize platform-dependent inputs (path separators, POSIX conversion) and casing/shape (schema type recursion) before processing; don’t let environment differences leak into logic.
- **Invariant-based estimators:** Ensure estimates depend on the correct dimensions (e.g., image count not base64 byte length). Add tests that compare estimates across irrelevant payload size changes.
- **Property/fuzz where stateful/sequence-driven:** For state transitions driven by user/agent actions, fuzz random verb sequences and assert invariants (e.g., “skip hides only its row”, “undo restores”).
- **Complexity guards:** Cap sizes/depths and avoid constructs that can degrade badly on long inputs (e.g., backtracking-heavy patterns); enforce timeouts and maximum expansions.

Example (token/estimation invariant test):
```ts
const base = estimateRequestInputTokens({
  messages: [{ role: "user", content: [{ type: "image", data: "A", mediaType: "image/png" }] }],
});
const huge = estimateRequestInputTokens({
  messages: [{ role: "user", content: [{ type: "image", data: "A".repeat(500_000), mediaType: "image/png" }] }],
});
// Payload length must not move the estimate.
expect(huge).toBe(base);
```

If you adopt this standard, subtle bugs like incorrect cursor movement, lost rename identity, broken schema recursion, or payload-size-dependent estimators are far less likely to slip through review.