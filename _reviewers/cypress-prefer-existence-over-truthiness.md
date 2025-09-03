---
title: prefer existence over truthiness
description: Use explicit existence checks instead of truthiness checks when dealing
  with object properties, null/undefined values, or when falsy values are valid data.
repository: cypress-io/cypress
label: Null Handling
language: TypeScript
comments_count: 4
repository_stars: 48850
---

Use explicit existence checks instead of truthiness checks when dealing with object properties, null/undefined values, or when falsy values are valid data.

Truthiness checks can cause bugs in several scenarios:
1. **Object properties containing objects/promises** - These are always truthy even when you want to check existence
2. **Falsy but valid values** - Values like `0`, `""`, or `false` that should be processed but fail truthiness checks
3. **Null vs undefined distinction** - When you need to handle both null and undefined consistently

**Examples:**

```typescript
// ❌ Bad: Promise objects are always truthy
if (fileProcessors[filePath]) {
  return fileProcessors[filePath]
}

// ✅ Good: Check for property existence
if (filePath in fileProcessors) {
  return fileProcessors[filePath]
}

// ❌ Bad: Filters out valid falsy values like "0"
return trim ? dequote(_.trim(result)) : result

// ✅ Good: Only filter out null/undefined
return trim && result != null ? dequote(_.trim(result)) : result

// ❌ Bad: Boolean true is falsy in this context check
if (keyEntry === undefined) {
  // handle undefined case
}

// ✅ Good: Explicit check avoids confusion with boolean values
if (!keyEntry) {
  // This would incorrectly trigger for boolean false
}
```

Use `in` operator for object property existence, `!= null` for null/undefined checks when falsy values are valid, and be explicit about what condition you're actually testing for.