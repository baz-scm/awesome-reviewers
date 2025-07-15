---
title: Maintain consistent code style
description: "Follow project-wide code style conventions to ensure consistency and\
  \ readability. Key practices include:\n\n1. Use consistent spacing and formatting:\n\
  \   - Maintain blank lines between test cases"
repository: vuejs/core
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 50769
---

Follow project-wide code style conventions to ensure consistency and readability. Key practices include:

1. Use consistent spacing and formatting:
   - Maintain blank lines between test cases
   - Proper indentation and line breaks for imports
   - Follow established quote style (single vs double)

2. Prefer clean control flow:
   - Use early returns instead of nested if/else chains
   - Avoid unnecessary conditional nesting

Example of clean control flow:
```typescript
// Instead of:
function isCoreComponent(tag: string): symbol | void {
  if (isBuiltInType(tag, 'Teleport')) {
    return TELEPORT
  } else if (isBuiltInType(tag, 'Suspense')) {
    return SUSPENSE
  } else if (isBuiltInType(tag, 'KeepAlive')) {
    return KEEP_ALIVE
  }
}

// Prefer:
function isCoreComponent(tag: string): symbol | void {
  if (isBuiltInType(tag, 'Teleport')) {
    return TELEPORT
  }
  if (isBuiltInType(tag, 'Suspense')) {
    return SUSPENSE
  }
  if (isBuiltInType(tag, 'KeepAlive')) {
    return KEEP_ALIVE
  }
}
```

Use automated tools like ESLint and Prettier to enforce consistent formatting. When making changes, ensure they align with the existing codebase style rather than introducing new patterns.