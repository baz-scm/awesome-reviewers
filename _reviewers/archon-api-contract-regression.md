---
title: API contract regression
description: 'When adding or changing API-like functions (parsers, clients, helpers),
  treat them as having a stable contract: define the accepted inputs and exact output
  shape, cover tricky edge cases with regression tests, and remove/deprecate superseded
  code paths so the API surface stays unambiguous.'
repository: coleam00/Archon
label: API
language: TypeScript
comments_count: 2
repository_stars: 21089
---

When adding or changing API-like functions (parsers, clients, helpers), treat them as having a stable contract: define the accepted inputs and exact output shape, cover tricky edge cases with regression tests, and remove/deprecate superseded code paths so the API surface stays unambiguous.

How to apply:
- Specify the contract: what the function accepts (e.g., URL vs path formats; SSR/browser contexts) and the exact return fields.
- Add regression tests for known gaps: include edge-case inputs (e.g., relative paths, UNC paths) and verify the output shape.
- If an implementation/API was replaced, delete or clearly deprecate the old one—avoid leaving “dead code” that suggests multiple behaviors.

Example (contract + regression):
```ts
// Contract: treat GitHub URLs as { url } and local/UNC paths as { path }
function getCodebaseInput(input: string): { url?: string; path?: string } {
  // ...implementation
  return {};
}

// Regression cases for gaps
test('treats relative paths as paths', () => {
  expect(getCodebaseInput('../repo')).toEqual({ path: '../repo' });
});

test('treats UNC paths as paths', () => {
  expect(getCodebaseInput('\\server\\share\\repo')).toEqual({
    path: '\\server\\share\\repo',
  });
});
```

Checklist:
- Do we have tests that pin the contract for edge cases?
- Is the old implementation removed/deprecated after replacement?
- Do return types/fields remain consistent across contexts (SSR vs browser, URL vs path)?