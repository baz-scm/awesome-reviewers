---
title: Follow snake_case convention
description: Consistently use snake_case naming throughout the codebase for variables,
  methods, and identifiers to maintain established conventions. When the codebase
  has adopted snake_case as the standard, all new code should follow this pattern
  rather than introducing camelCase or other naming styles.
repository: sveltejs/svelte
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 83580
---

Consistently use snake_case naming throughout the codebase for variables, methods, and identifiers to maintain established conventions. When the codebase has adopted snake_case as the standard, all new code should follow this pattern rather than introducing camelCase or other naming styles.

Example:
```typescript
// Preferred - follows codebase snake_case convention
const class_name = `__svelte_${hash(rule)}`;
function push_quasi(q: string) { ... }

// Avoid - inconsistent with established convention
const className = `__svelte_${hash(rule)}`;
function pushQuasi(q: string) { ... }
```

This ensures consistency across the codebase, improves readability, and prevents confusion when different naming conventions are mixed within the same project.