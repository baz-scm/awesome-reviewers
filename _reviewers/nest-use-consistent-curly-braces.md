---
title: Use consistent curly braces
description: Always use curly braces for conditional statements and loops, even for
  single-line bodies. This maintains consistency throughout the codebase and improves
  readability. Avoid inline conditionals.
repository: nestjs/nest
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 71767
---

Always use curly braces for conditional statements and loops, even for single-line bodies. This maintains consistency throughout the codebase and improves readability. Avoid inline conditionals.

Instead of:
```typescript
if (areThereNoFileIn && this.fileIsRequired) return;
if (this.moduleTokenCache.has(key)) return this.moduleTokenCache.get(key);
```

Use:
```typescript
if (areThereNoFileIn && this.fileIsRequired) {
  return;
}
if (this.moduleTokenCache.has(key)) {
  return this.moduleTokenCache.get(key);
}
```

This style:
- Maintains consistent formatting across the codebase
- Makes code more readable and maintainable
- Reduces the risk of errors when modifying conditions
- Makes it easier to add additional statements later without restructuring