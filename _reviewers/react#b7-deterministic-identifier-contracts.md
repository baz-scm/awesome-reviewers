---
title: Deterministic Identifier Contracts
description: 'When code depends on identifier shape or naming conventions, treat naming
  as an explicit contract: validate input identifiers, apply deterministic transformations
  within the correct deduplication/scope boundaries, and enforce assumptions early.'
repository: facebook/react#b7
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 251888
---

When code depends on identifier shape or naming conventions, treat naming as an explicit contract: validate input identifiers, apply deterministic transformations within the correct deduplication/scope boundaries, and enforce assumptions early.

Guidelines:
- Validate before transforming: only apply “component vs host” / identifier-sanitization logic to inputs you can actually receive (e.g., rely on parser guarantees, and make comments precise about the valid input domain).
- Preserve required original names: for JSX attributes that are not valid JS identifiers (e.g. `aria-label`), keep the original prop key at the call site and use a quoted destructuring key when needed.
- Generate names deterministically and safely: prefer the intended UID/name-generation APIs and deduplication boundaries for the transformation scope; avoid approaches that over-fire and cause snapshot/eval regressions.
- Test naming heuristics: if behavior changes based on naming conventions (e.g. PascalCase component detection), add tests for both valid and tricky wrapper patterns.
- Fail fast on identifier-shape assumptions: use invariants/type checks to ensure you only proceed with named identifiers when required.

Example (hyphenated JSX prop preservation):
```ts
function isHyphenatedJsxProp(originalName: string): boolean {
  return (!isValidIdentifier(originalName) && /^[a-zA-Z_][\w.-]*$/.test(originalName));
}

// Later when destructuring from temp:
// const { "aria-label": ariaLabel } = t0; // keep quoted original key
```