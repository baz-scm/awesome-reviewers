---
title: Preserve Transform Invariants
description: When implementing algorithms that transform external/structured data
  (parsers, token estimators, schema normalizers, cap/limit calculators), base correctness
  on explicit semantic invariants—not on incidental formatting, payload size, or shallow
  structure.
repository: cline/cline#v13
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 70874
---

When implementing algorithms that transform external/structured data (parsers, token estimators, schema normalizers, cap/limit calculators), base correctness on explicit semantic invariants—not on incidental formatting, payload size, or shallow structure.

Standards:
- Parse with delimiter/record rules that match the spec exactly; never “split all delimiters” if only specific segments matter. Add tests for delimiters that can appear inside content.
- Define semantic invariants up front (e.g., “image token cost depends on image count, not base64 length”; “nested `type` normalization applies at every depth”; “default cap is a floor, not a ceiling unless model budgeting warrants it”).
- Ensure recursion/branch handling covers all relevant structural forms (arrays/items, combinators, unions). Don’t apply gating logic before reaching nested branches.
- For clamping/cap logic, document and preserve the intended order: caller overrides vs defaults, then model/context clamps.
- Add tests that lock the invariants under adversarial inputs (large payloads, delimiter-in-content, nested schemas) and—where stateful sequences exist—use targeted sequence tests and fuzzing.

Example pattern (token/cap invariants):
```ts
const baseDefault = input.defaultMaxOutputTokens ?? DEFAULT_GATEWAY_MAX_OUTPUT_TOKENS;
const catalogDefault =
  input.defaultMaxOutputTokens === undefined && isPositiveFiniteNumber(input.model.maxOutputTokens)
    ? Math.max(
        baseDefault,
        Math.floor(input.model.maxOutputTokens * DEFAULT_GATEWAY_MAX_OUTPUT_FRACTION),
      )
    : baseDefault;
// then apply remaining model/context clamping afterwards
```