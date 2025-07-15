---
title: "Standardize null value checks"
description: "Always use consistent patterns and utility functions for handling null and undefined values. This improves code reliability and maintainability while preventing common errors."
repository: "axios/axios"
label: "Null Handling"
language: "JavaScript"
comments_count: 5
repository_stars: 107000
---

Always use consistent patterns and utility functions for handling null and undefined values. This improves code reliability and maintainability while preventing common errors.

Key guidelines:
1. Use utility functions (like isUndefined, isNull) instead of direct comparisons
2. Prefer empty collections over null for container types
3. Use explicit null checks when dealing with potentially undefined objects

Example:
```javascript
// ❌ Avoid direct null/undefined checks
if (typeof value === 'undefined' || value === null) {
  // ...
}

// ✅ Use utility functions
if (utils.isUndefined(value) || utils.isNull(value)) {
  // ...
}

// ❌ Avoid setting null for collections
this.handlers = null;

// ✅ Use empty collections instead
this.handlers = [];

// ❌ Avoid unsafe property access
if (payload && payload.isAxiosError) {
  // ...
}

// ✅ Use comprehensive null checks
if (!!payload && typeof payload === 'object' && payload.isAxiosError) {
  // ...
}
```