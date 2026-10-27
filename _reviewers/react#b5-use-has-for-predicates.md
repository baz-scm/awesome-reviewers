---
title: Use Has For Predicates
description: 'Adopt a semantic naming rule for boolean helpers: if the function reports
  whether something *exists* (e.g., “any detail has severity X”, “any prop collides
  after sanitization”), name it with `hasX()`/`containsX()` rather than `isX()`. Reserve
  `isX()` for clear single-state predicates (e.g., “the compiler is in an invariant
  state”). This prevents confusing...'
repository: facebook/react#b5
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 251886
---

Adopt a semantic naming rule for boolean helpers: if the function reports whether something *exists* (e.g., “any detail has severity X”, “any prop collides after sanitization”), name it with `hasX()`/`containsX()` rather than `isX()`. Reserve `isX()` for clear single-state predicates (e.g., “the compiler is in an invariant state”). This prevents confusing APIs when the return value depends on scanning multiple elements.

**Before**
```ts
class CompilerError {
  isError(): boolean { /* true if any detail has severity Error */ }
  isWarning(): boolean { /* true if no errors and any warning */ }
}
```

**After**
```ts
class CompilerError {
  hasError(): boolean { /* any detail severity === Error */ }
  hasWarning(): boolean { /* no errors and any detail severity === Warning */ }
}
```

Also ensure identifier-related helpers and comments are precise about their domain (e.g., “only valid identifiers reach this branch” vs “all identifiers”), so the naming of helpers matches what the code actually handles.