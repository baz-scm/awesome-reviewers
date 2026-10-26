---
title: Prefer semantic and safe names
description: 'Adopt naming rules that make identifiers/predicates both correct and
  predictable.


  1) Generated identifier naming

  - Use the compiler/runtime’s canonical unique-ID generator for new symbols (e.g.,
  prefer the context’s `newUuid()`/uid API rather than ad-hoc sets when uniqueness/dedup
  boundaries are unclear).'
repository: facebook/react#b2
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 251882
---

Adopt naming rules that make identifiers/predicates both correct and predictable.

1) Generated identifier naming
- Use the compiler/runtime’s canonical unique-ID generator for new symbols (e.g., prefer the context’s `newUuid()`/uid API rather than ad-hoc sets when uniqueness/dedup boundaries are unclear).
- When sanitizing names (e.g., JSX attributes like `aria-label`), transform deterministically and only as needed; ensure the final identifier is valid, otherwise fall back to a safe prefix (e.g., `_`).
- Keep shadowing behavior intentional and scope-local to avoid fixture-breaking renames.

2) Boolean helper naming
- Use `isX()` only when the predicate represents a single overall state.
- Use `hasX()` when the logic checks whether *any* element in a collection matches (existential checks across multiple details).

Example (boolean helpers):
```ts
// Prefer when checking for existence across details
hasError(): boolean {
  return this.details.some(d => d.severity === ErrorSeverity.Error);
}

// Reserve isX() for whole-object state
isWarningOnly(): boolean {
  return this.details.every(d => d.severity === ErrorSeverity.Off || d.severity === ErrorSeverity.Warning)
      && this.details.some(d => d.severity === ErrorSeverity.Warning);
}
```

This reduces misleading APIs and prevents naming changes from causing collisions or unintended snapshot/output differences.