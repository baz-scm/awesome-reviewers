---
title: Consistent language in naming
description: Use a single language (preferably English) consistently throughout your
  codebase for all identifiers including interface names, classes, variables, and
  properties. Avoid mixing languages as this reduces code readability and creates
  inconsistent naming patterns.
repository: appwrite/appwrite
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 51959
---

Use a single language (preferably English) consistently throughout your codebase for all identifiers including interface names, classes, variables, and properties. Avoid mixing languages as this reduces code readability and creates inconsistent naming patterns.

**Before:**
```typescript
export interface ModeloBaseDeDatos {
    $id: string;
    name: string;
    permissions: string[];
    // Otros campos: createdAt, updatedAt, etc.
}
```

**After:**
```typescript
export interface DatabaseModel {
    $id: string;
    name: string;
    permissions: string[];
    createdAt: string;
    updatedAt: string;
    enabled?: boolean;
}
```

This standard improves code maintainability and helps prevent confusion, especially in projects with international contributors. When choosing names, prefer English for broader accessibility and alignment with most programming languages and frameworks.