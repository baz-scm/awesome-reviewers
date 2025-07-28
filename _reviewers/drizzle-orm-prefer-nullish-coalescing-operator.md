---
title: prefer nullish coalescing operator
description: Use the nullish coalescing operator (`??`) instead of the logical OR
  operator (`||`) when you specifically want to provide fallback values only for `null`
  or `undefined`, not for other falsy values.
repository: drizzle-team/drizzle-orm
label: Null Handling
language: TypeScript
comments_count: 5
repository_stars: 29461
---

Use the nullish coalescing operator (`??`) instead of the logical OR operator (`||`) when you specifically want to provide fallback values only for `null` or `undefined`, not for other falsy values.

The logical OR operator (`||`) treats all falsy values (empty strings, 0, false, null, undefined) as conditions to use the fallback value. The nullish coalescing operator (`??`) only triggers the fallback for `null` and `undefined`, preserving other falsy values that might be valid data.

**Use `??` when:**
- Empty strings, 0, or false are valid values that shouldn't trigger fallbacks
- You're specifically handling null/undefined cases
- Working with optional properties or nullable database fields

**Examples:**

```typescript
// ❌ Problematic - empty string triggers fallback to 'public'
const typeSchema = column.enum.schema || 'public';

// ✅ Correct - only null/undefined triggers fallback
const typeSchema = column.enum.schema ?? 'public';

// ❌ Problematic - treats null as invalid when it might be valid data
if (!!set[colName]) { /* ... */ }

// ✅ Correct - explicitly check for undefined
if (set[colName] !== undefined) { /* ... */ }

// ❌ Problematic - empty object created for any falsy value
Object.keys(obj || {})

// ✅ Correct - empty object only for null/undefined
Object.keys(obj ?? {})
```

This pattern is especially important when working with database schemas, optional configurations, and API responses where distinguishing between "no value provided" (null/undefined) and "falsy value provided" (empty string, 0, false) is crucial for correct behavior.