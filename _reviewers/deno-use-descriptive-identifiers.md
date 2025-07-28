---
title: Use descriptive identifiers
description: Choose names that clearly communicate the purpose, functionality, and
  usage context of variables, methods, and types. Avoid ambiguous or overly generic
  names that require additional context to understand.
repository: denoland/deno
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 103714
---

Choose names that clearly communicate the purpose, functionality, and usage context of variables, methods, and types. Avoid ambiguous or overly generic names that require additional context to understand.

When naming:
- Include key functionality details in the name (e.g., `readWithCancelHandle` instead of a generic property)
- Consider the visibility and intended usage pattern (e.g., use symbols or naming conventions to indicate internal/private methods)
- Look to established conventions in similar libraries or codebases when uncertain
- If a name is causing confusion or debate, consider whether the abstraction itself needs restructuring

Example from codebase:
```typescript
// Instead of unclear property access:
if (this[kStreamBaseField]![_readCancel]) {

// Use descriptive method name:
if (this[kStreamBaseField]!.readWithCancelHandle()) {
```

Good naming reduces the need for comments and makes code self-documenting, improving maintainability and reducing cognitive load for other developers.