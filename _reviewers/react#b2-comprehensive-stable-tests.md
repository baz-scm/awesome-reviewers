---
title: Comprehensive, stable tests
description: When adding/adjusting correctness metadata or UI flows, ensure tests
  (1) validate invariants broadly and include edge cases, and (2) remain stable and
  deterministic.
repository: facebook/react#b2
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251882
---

When adding/adjusting correctness metadata or UI flows, ensure tests (1) validate invariants broadly and include edge cases, and (2) remain stable and deterministic.

Apply this as two rules:

1) Assert invariants globally in fixture/harness tests
- Don’t only test special subsets of nodes (e.g., `source-locations/`). If the output AST exposes range/loc fields, add a global assertion over the whole output tree.
- Include edge cases where declarations/nodes may omit `loc` (hoisted `let x;`, for-in/for-of declarators, etc.). Either add fixtures that cover the behavior you expect or explicitly track those missing `loc` cases as follow-ups.

Example invariant check pattern (adapt to your AST/node shape):
```ts
function assertRangesAcrossOutputAst(outputAst: any) {
  for (const node of walkOutputAst(outputAst)) {
    const { start, end, loc } = node ?? {};
    const hasNumericRange = typeof start === 'number' && typeof end === 'number';
    const hasIndex = loc?.index != null;
    if (!hasNumericRange || !hasIndex) continue;

    // Invariant: range maps exactly to loc index boundaries
    expect(start).toBe(loc.start.index);
    expect(end).toBe(loc.end.index);
    expect(start).toBeLessThanOrEqual(end);
  }
}
```

2) Make E2E tests deterministic and cover state variants
- Avoid brittle positional selectors like `nth(1)` / `nth(3)` for UI components that can shift.
- Prefer stable selectors (e.g., `data-testid`) for tabs/buttons and target elements by intent.
- Add coverage for meaningful UI/runtime state toggles (e.g., “internals shown” vs “internals hidden”).

Example selector guidance:
```ts
// Prefer data-testid over nth(...)
const editor = page
  .locator('[data-testid="config-tab"]')
  .locator('.monaco-editor');
const texts = await editor.allInnerTexts();
```

Outcome: correctness changes are guarded by broad invariant assertions (with edge-case fixtures), and UI tests don’t break due to incidental DOM/layout changes.