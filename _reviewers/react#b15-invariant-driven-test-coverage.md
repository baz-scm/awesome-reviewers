---
title: Invariant-Driven Test Coverage
description: When adding or changing behavior, make tests enforce the *actual invariant*
  (not just snapshots), ensure the invariant is validated across all supported implementations/paths,
  and avoid over-claiming coverage.
repository: facebook/react#b15
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251891
---

When adding or changing behavior, make tests enforce the *actual invariant* (not just snapshots), ensure the invariant is validated across all supported implementations/paths, and avoid over-claiming coverage.

Checklist for teams:
1) Assert invariants at the correct scope
- If you’re guaranteeing structural consistency (e.g., source ranges), add a global check in the shared harness/fixture runner so it applies to the whole output, not only a subset.

Example (range consistency style):
```ts
// In a shared fixture harness
for (const node of allOutputNodes(ast)) {
  if (typeof node.start === 'number' && typeof node.end === 'number' && node.loc?.index != null) {
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
}
```

2) Cover or explicitly document edge cases
- If a guarantee depends on inputs that may be missing (e.g., nodes without `loc` for hoisted/empty declarators), either add fixtures to cover those cases or record them as intentional exceptions/follow-ups.

3) Keep E2E tests stable and scenario-complete
- For UI flows, prefer dedicated selectors (e.g., `data-testid`) over position-dependent locators, and add at least one test for each meaningful mode toggle (e.g., “internals on/off”).
- Example selector pattern:
```ts
const editorTexts = await page
  .locator('[data-testid="config-tab"] .monaco-editor')
  .allInnerTexts();
```

Result: tests remain trustworthy as implementations evolve, prevent silent regressions across backends, and reduce flaky UI failures.