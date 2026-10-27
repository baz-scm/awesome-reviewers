---
title: Test Invariants And Scenarios
description: When a change affects semantics (codegen, mapping, typing, offsets),
  require tests that validate the underlying invariants across all relevant backends
  and through realistic inputs, and ensure e2e tests are deterministic.
repository: facebook/react#b6
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 251888
---

When a change affects semantics (codegen, mapping, typing, offsets), require tests that validate the underlying invariants across all relevant backends and through realistic inputs, and ensure e2e tests are deterministic.

**What to require in code review**
1. **Global invariant checks in shared harnesses (all backends):** If your output has structural fields (ranges, offsets, index links, loc info), assert consistency for *every* applicable node—not only special-case subsets.
2. **Targeted realistic tests for correctness risk:** If you relax/alter an assumption/invariant, add a minimal example using the real runtime/codegen path and (when applicable) run it through the type provider to confirm compilation behavior.
3. **Deterministic e2e selection + scenario coverage:** Avoid brittle “nth()”-style selectors; prefer stable `data-testid` selectors and add coverage for key toggles (e.g., feature on/off).

**Example invariant assertion (test/harness style)**
```ts
// In a shared test harness that runs for both backends
function assertOutputRanges(outputAst: any) {
  for (const node of walk(outputAst)) {
    const { start, end, loc } = node ?? {};
    if (typeof start === 'number' && typeof end === 'number' && loc?.index != null) {
      // Ensure output ranges align to loc indices and have sane ordering
      expect(start).toBe(loc.start.index);
      expect(end).toBe(loc.end.index);
      expect(start).toBeLessThanOrEqual(end);
    }
  }
}
```

**Example correctness-risk test idea**
- Add a minimal shared-runtime function that exercises the receiver/return pattern you’re concerned about, then compile/typecheck it via the real type provider to confirm no regression.

**Example e2e reliability improvement**
- Replace selection like `nth(3)` with stable locators, e.g.:
  - `page.locator('[data-testid="config-tab"] .monaco-editor')`
  - Add the same test with the app started in both modes (internals shown vs hidden).