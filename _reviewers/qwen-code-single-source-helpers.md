---
title: Single Source Helpers
description: When code review finds duplicated logic or repeated formatting/constants,
  treat it as a “single source of truth” violation. Factor shared logic into a helper/module
  and reuse it everywhere; avoid hardcoded literals where an existing helper/constant
  exists; and keep established idioms consistent.
repository: QwenLM/qwen-code
label: Code Style
language: TypeScript
comments_count: 11
repository_stars: 26407
---

When code review finds duplicated logic or repeated formatting/constants, treat it as a “single source of truth” violation. Factor shared logic into a helper/module and reuse it everywhere; avoid hardcoded literals where an existing helper/constant exists; and keep established idioms consistent.

Guidelines:
- **Duplicate logic across code paths** (e.g., launch vs resume, attach vs subscribe) should be extracted into a shared helper function placed near related constants/contracts.
- **Duplicate protocol/type definitions** should be aliased to one canonical type (e.g., `type New = Old;`) or imported from a shared module.
- **Hardcoded strings/format separators used for assertions or UI formatting** should become shared constants (or reuse an existing formatter helper) so updates don’t require hunting multiple sites.
- **Maintain consistent style/idioms** for readability (e.g., prefer the existing `timer.unref?.()` pattern over verbose type guards when they’re equivalent).
- **Don’t keep misleading no-op steps** (e.g., assigning `undefined` immediately overwritten on the next line); remove dead assignments when refactoring.

Example (helper extraction):
```ts
// helpers.ts
export function extractParentToolNames(generationConfig: unknown): string[] {
  // ... shared extraction logic ...
  return names;
}

// call sites
const names = extractParentToolNames(generationConfig);
```

Example (constant for repeated literals in tests):
```ts
const INITIAL_CONTENT = 'original content';
expect(input.content).not.toBe(INITIAL_CONTENT);
```