---
title: Remove commented out code
description: Delete commented-out code instead of retaining it in the codebase. Commented
  code creates confusion, adds maintenance overhead, and clutters the source files.
  If code is no longer needed, remove it entirely - version control systems will preserve
  the history if it needs to be referenced later.
repository: elie222/inbox-zero
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 8267
---

Delete commented-out code instead of retaining it in the codebase. Commented code creates confusion, adds maintenance overhead, and clutters the source files. If code is no longer needed, remove it entirely - version control systems will preserve the history if it needs to be referenced later.

Example of what to avoid:
```typescript
// export function isActionError(error: any): error is ActionError {
//   return error && typeof error === "object" && "error" in error && error.error;
// }

export function newFunction() {
  // Implementation
}
```

Instead, simply delete unused code:
```typescript
export function newFunction() {
  // Implementation
}
```

If you need to temporarily disable code during development:
1. Use feature flags or environment variables for toggling functionality
2. Create a separate branch for experimental changes
3. Use TODO comments to mark incomplete work, but don't retain commented implementation

This keeps the codebase clean, reduces cognitive load when reading code, and prevents outdated commented code from becoming misleading over time.