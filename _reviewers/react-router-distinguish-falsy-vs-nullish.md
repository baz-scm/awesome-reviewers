---
title: distinguish falsy vs nullish
description: When handling potentially null or undefined values, carefully choose
  between the logical OR (`||`) and nullish coalescing (`??`) operators based on whether
  you want to preserve other falsy values.
repository: remix-run/react-router
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 55270
---

When handling potentially null or undefined values, carefully choose between the logical OR (`||`) and nullish coalescing (`??`) operators based on whether you want to preserve other falsy values.

The `||` operator treats all falsy values (null, undefined, false, 0, "", NaN) as "missing" and provides the fallback. The `??` operator only treats null and undefined as "missing", preserving other falsy values like empty strings or false booleans.

**Use `||` when:** You want to reject all falsy values and provide a default.
```javascript
// Reject empty strings, use default
pathname: locationProp.pathname || "/"
```

**Use `??` when:** You want to preserve legitimate falsy values but handle null/undefined.
```javascript
// Allow false, "", 0 but handle null/undefined
state: locationProp.state ?? null
```

**Avoid `||` when falsy values are valid:** Using `||` can cause bugs by rejecting legitimate values.
```javascript
// BAD: Rejects "", false, 0, NaN as valid state values
state: locationProp.state || null

// GOOD: Only rejects null/undefined
state: locationProp.state ?? null
```

Consider bundle size implications when using `??` in environments with older transpilation targets, and use explicit null checks as an alternative: `value != null ? value : fallback`.