---
title: Use consistent control structures
description: Always use curly braces for control structures (if, for, while, etc.),
  even for single-line statements. This improves code readability and maintainability
  by making the code structure explicit and consistent.
repository: nestjs/nest
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 71766
---

Always use curly braces for control structures (if, for, while, etc.), even for single-line statements. This improves code readability and maintainability by making the code structure explicit and consistent.

Example:
```typescript
// Incorrect
if (areThereNoFileIn && this.fileIsRequired) return;

// Correct
if (areThereNoFileIn && this.fileIsRequired) {
  return;
}

// Incorrect
if (this.flushLogsOnOverride) this.flushLogs();

// Correct
if (this.flushLogsOnOverride) {
  this.flushLogs();
}
```

This style:
- Prevents errors when adding more statements later
- Makes code structure immediately clear
- Maintains consistency across the codebase
- Makes code reviews more efficient by eliminating style discussions
- Reduces cognitive load when reading code