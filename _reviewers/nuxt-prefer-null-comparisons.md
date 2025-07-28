---
title: prefer != null comparisons
description: When checking for null or undefined values, prefer the concise `!= null`
  comparison over explicit checks or array-based methods. This pattern effectively
  handles both null and undefined while preserving other falsy values like `false`,
  `0`, or empty strings.
repository: nuxt/nuxt
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 57769
---

When checking for null or undefined values, prefer the concise `!= null` comparison over explicit checks or array-based methods. This pattern effectively handles both null and undefined while preserving other falsy values like `false`, `0`, or empty strings.

The `!= null` pattern is more readable and performant than alternatives:

```javascript
// Preferred: Concise and clear
const hasCachedData = () => options.getCachedData!(key) != null

// Avoid: Verbose explicit checks
const hasCachedData = () => {
  const data = options.getCachedData!(key)
  return data !== null && data !== undefined
}

// Avoid: Array-based inclusion checks
const hasCachedData = () => ![null, undefined].includes(options.getCachedData!(key) as any)
```

For cases requiring additional type safety, combine null checks with type validation:

```javascript
// Good: Null check with type validation
if (!rawVersion || typeof rawVersion !== 'string') {
  return
}

// Good: Explicit equality for specific values
if (result === true) {
  // Handle confirmed true, not just truthy
}
```

This approach maintains null safety while keeping code concise and avoiding unnecessary complexity in most common scenarios.