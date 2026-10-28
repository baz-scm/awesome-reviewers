---
title: Cover algorithmic edge cases
description: When writing algorithms that parse, match, or transform structured data
  (git output, YAML frontmatter, JSON numbers, text matching, stateful cursors), explicitly
  enumerate the edge cases the input format or domain can produce — duplicates, overlapping
  identifiers, special-case formats (submodules, renames, block vs. inline scalars),...
repository: 'cline/cline

  '
label: Algorithms
language: TypeScript
comments_count: 7
repository_stars: 70942
---

When writing algorithms that parse, match, or transform structured data (git output, YAML frontmatter, JSON numbers, text matching, stateful cursors), explicitly enumerate the edge cases the input format or domain can produce — duplicates, overlapping identifiers, special-case formats (submodules, renames, block vs. inline scalars), boundary/precision-sensitive values, and stale/out-of-order state — and verify the algorithm's behavior against the real tool or spec it mirrors rather than an assumed simplified model. Favor correctness mechanisms that are structurally guaranteed over ones that merely happen to work for common inputs: e.g., match on stable identifiers instead of positions (skip/unskip acting on `itemId`, not list index), disambiguate by scope/order instead of first-match (finding a sent prompt only among messages after the run count it was sent at), and preserve exact source representation when round-tripping values that have multiple valid textual spellings (keep original JSON text when decoding a number would change its spelling, e.g. large IDs, high-precision decimals, negative zero). Each identified edge case should have a corresponding regression test, for example:

```ts
// Preserve exact numeric spelling across parse/stringify
test("keeps original text when decoding changes the number's spelling", () => {
  const source = '{"id": 9007199254740993}'; // loses precision as JS number
  expect(expandRecoveryJson(source)).toContain("9007199254740993");
});
```

Apply this standard whenever an algorithm's correctness depends on the shape of real-world input rather than on abstract logic alone: add targeted tests for each discovered edge case, and prefer designs (stable ids, explicit scoping, original-text preservation) that eliminate whole classes of edge cases rather than patching them individually.