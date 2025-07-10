---
title: Consistent descriptive naming
description: Use naming conventions that are both consistent with existing patterns
  and descriptively clear about purpose. Follow established patterns in the codebase
  for similar entities while ensuring names are specific and self-explanatory.
repository: langfuse/langfuse
label: Naming Conventions
language: Prisma
comments_count: 2
repository_stars: 13574
---

Use naming conventions that are both consistent with existing patterns and descriptively clear about purpose. Follow established patterns in the codebase for similar entities while ensuring names are specific and self-explanatory.

Example from Prisma schema:
```
// Avoid this:
model Project {
  // Inconsistent casing (camelCase vs PascalCase)
  Dashboard              Dashboard[]
  actions                Action[]      // Inconsistent
  
  // Generic, unclear name
  SavedView              SavedView[]   // Too generic
}

// Prefer this:
model Project {
  // Consistent casing pattern
  Dashboard              Dashboard[]
  Actions                Action[]      // Consistent
  
  // Specific, descriptive name
  TableViewPreset        TableViewPreset[]  // Clear purpose
}
```

When adding new fields, models, or variables, check existing related elements and follow their naming pattern. If existing names are unclear, consider refactoring them to be more descriptive about their function and context.