---
title: Use null strategically
description: When handling empty or missing values, be intentional about using `null`,
  `undefined`, or empty strings based on how downstream systems interpret these values.
  In particular, when working with database operations (like PostgreSQL), use `null`
  instead of empty strings for fields that need to be cleared or constraints that
  should be dropped.
repository: supabase/supabase
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 86070
---

When handling empty or missing values, be intentional about using `null`, `undefined`, or empty strings based on how downstream systems interpret these values. In particular, when working with database operations (like PostgreSQL), use `null` instead of empty strings for fields that need to be cleared or constraints that should be dropped.

```typescript
// Bad: Using empty string or keeping values as-is
const comment = ((field.comment?.length ?? '') === 0 ? '' : field.comment)?.trim()
const check = field.check?.trim()

// Good: Converting empty values to null for database operations
const comment = field.comment?.trim() || null
const check = field.check?.trim() || null
```

This pattern ensures proper behavior when working with systems that treat null specially. For PostgreSQL specifically, NULL is required to remove comments or constraints, as empty strings are treated differently. Use the nullish coalescing operator (`||`) with null to handle this pattern concisely.