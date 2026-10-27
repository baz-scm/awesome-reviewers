---
title: Invariant Fixtures and Stable Selectors
description: When adding/adjusting tests, validate *global correctness invariants*
  with fixtures across all relevant implementations, and ensure E2E/UI tests use *deterministic
  selectors*.
repository: facebook/react#b7
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251888
---

When adding/adjusting tests, validate *global correctness invariants* with fixtures across all relevant implementations, and ensure E2E/UI tests use *deterministic selectors*.

Apply this as:
1) **Assert output-wide invariants (not a narrow slice).** For compiler/transform output, add a shared check that walks the full output AST and verifies range/loc consistency for every node that should carry it (e.g., numeric `start/end` matching `loc.*.index`, plus ordering like `start <= end`). Run the same checks for every backend.
2) **Cover edge cases where metadata may be missing.** If some nodes (e.g., hoisted declarations or specific syntax forms) legitimately lack `loc`, don’t silently accept them—either add fixtures that exercise them and confirm expected behavior, or explicitly track them as follow-ups with corresponding fixtures.
3) **Make E2E tests resilient.** Avoid brittle locators like `.nth(k)` for UI elements. Prefer stable selectors (e.g., `data-testid`) and add coverage for meaningful UI modes/states (e.g., with/without “internals showing”).

Example patterns:
- Range invariant fixture (conceptual):
```ts
for (const node of outputAst.nodes()) {
  if (typeof node.start === 'number' && typeof node.end === 'number' && node.loc?.index != null) {
    assert(node.start === node.loc.start.index);
    assert(node.end === node.loc.end.index);
    assert(node.start <= node.end);
  }
}
```
- Stable E2E selection (conceptual):
```ts
await page.locator('[data-testid="config-tab"] .monaco-editor').allInnerTexts();
```

This prevents regressions from partial checks, makes known gaps visible via fixtures, and reduces test flakiness from UI layout/ordering changes.