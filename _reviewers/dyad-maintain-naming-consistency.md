---
title: Maintain naming consistency
description: Ensure naming follows consistent patterns within the codebase and adheres
  to official framework conventions. When creating related types or functions, use
  matching naming schemes to maintain clarity and prevent synchronization issues.
  Prefer established conventions over custom variations unless there's a compelling
  reason to deviate.
repository: dyad-sh/dyad
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 16903
---

Ensure naming follows consistent patterns within the codebase and adheres to official framework conventions. When creating related types or functions, use matching naming schemes to maintain clarity and prevent synchronization issues. Prefer established conventions over custom variations unless there's a compelling reason to deviate.

For example, if you have `CloneRepoParams`, create a corresponding `CloneRepoReturnType` rather than using a generic return type. Similarly, when working with frameworks like Supabase, stick to their official `function-name/index.ts` convention rather than implementing broader custom patterns.

```typescript
// Good: Consistent naming pattern
interface CloneRepoParams { ... }
interface CloneRepoReturnType { ... }

// Good: Following official convention
// supabase/functions/my-function/index.ts

// Avoid: Inconsistent or custom naming
interface CloneRepoParams { ... }
interface GenericResponse { ... } // Should be CloneRepoReturnType
```

This approach reduces cognitive load, prevents naming conflicts, and ensures the codebase remains maintainable as it scales.