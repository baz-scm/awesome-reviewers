---
title: Expand Fixture-Based Coverage
description: When logic affects compiler/codegen output (ranges/loc, member-expression
  reconstruction, or compilation invariants), update tests to cover the full relevant
  surface area and key edge cases—across all backends—and make E2E tests deterministic.
repository: facebook/react#b8
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 251889
---

When logic affects compiler/codegen output (ranges/loc, member-expression reconstruction, or compilation invariants), update tests to cover the full relevant surface area and key edge cases—across all backends—and make E2E tests deterministic.

Apply this as a checklist:
- Broaden assertions to the entire produced structure (e.g., validate `start/end` against `loc.*.index` for every applicable output node, not only declarations).
- Add/extend fixtures for known uncovered cases (e.g., declarations that legally omit `loc`, hoisted `let x;`, for-in/of declarators with missing `loc`). If you can’t fix now, add follow-up fixtures explicitly.
- Ensure parity: run the same fixture/harness coverage for both backends and fail the change if they diverge.
- If invariants were relaxed or control-flow changed, add a minimal typed runtime example that would have failed before (construct the method/call shape and verify compilation via the type provider).
- For E2E/UI tests, avoid brittle positional selectors (`nth(...)`). Add stable `data-testid` hooks (and test both initial UI modes/state variants).

Example (fixture/harness range assertion idea):
```ts
for (const node of allOutputNodes(ast)) {
  const hasNumeric = typeof node.start === 'number' && typeof node.end === 'number';
  const hasLocIndex = node.loc?.index != null && node.loc?.start?.index != null && node.loc?.end?.index != null;
  if (hasNumeric && hasLocIndex) {
    invariant(node.start === node.loc.start.index);
    invariant(node.end === node.loc.end.index);
    invariant(node.start <= node.end);
  }
}
```