---
title: Strict null checks
description: Use explicit strict equality checks when testing for null or undefined
  values. Prefer `x === undefined` over `typeof x === 'undefined'` when the variable
  is known to exist. When checking for both null and undefined, use `x == null` (loose
  equality) as it covers both cases, or check each explicitly with `x === null ||
  x === undefined`. Avoid using the `||`...
repository: facebook/yoga
label: Null Handling
language: JavaScript
comments_count: 5
repository_stars: 18255
---

Use explicit strict equality checks when testing for null or undefined values. Prefer `x === undefined` over `typeof x === 'undefined'` when the variable is known to exist. When checking for both null and undefined, use `x == null` (loose equality) as it covers both cases, or check each explicitly with `x === null || x === undefined`. Avoid using the `||` operator for fallback values when legitimate falsy values (like 0, false, or empty strings) are expected, as they will incorrectly trigger the fallback.

```javascript
// Good - explicit undefined check
if (value !== undefined) {
  return value;
}

// Good - covers both null and undefined
if (value != null) {
  return value;
}

// Bad - unnecessary typeof when variable exists
if (typeof value !== 'undefined') {
  return value;
}

// Bad - loses legitimate falsy values
return node.style.marginTop || node.style.margin; // 0 becomes fallback value

// Good - explicit existence check
return 'marginTop' in node.style ? node.style.marginTop : node.style.margin;
```