---
title: Explicit null/undefined checks
description: Use explicit, strict checks for null and undefined rather than relying
  on loose equality or ambiguous truthy checks, since these can silently conflate
  the two values or match unintended built-in properties. For example, prefer `val
  !== null && val !== undefined` over `null != val` when both cases must be handled,
  and use `val === null` (not `!=`) when only...
repository: tj/commander.js#CANARY-1ebfbbf4
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 28444
---

Use explicit, strict checks for null and undefined rather than relying on loose equality or ambiguous truthy checks, since these can silently conflate the two values or match unintended built-in properties. For example, prefer `val !== null && val !== undefined` over `null != val` when both cases must be handled, and use `val === null` (not `!=`) when only null should be excluded so undefined is still processed correctly. Likewise, avoid `typeof x !== 'undefined'` when a direct `x !== undefined` or `Object.prototype.hasOwnProperty` check is simpler and equally safe.

Before accessing properties or invoking methods on a potentially nullable value, guard against `null` explicitly—`typeof value === 'object'` is true for `null`, so always add `value !== null` before further inspection (e.g. `typeof value.toString === 'function'`) to avoid runtime crashes:

```js
// Bad: crashes if value is null
if (typeof value === 'object' && value.toString !== Object.prototype.toString) { ... }

// Good: explicit null guard
if (typeof value === 'object' && value !== null &&
    typeof value.toString === 'function' &&
    value.toString !== Object.prototype.toString) { ... }
```

When checking for the presence of a property or option that may be a built-in or inherited value (e.g., via prototype chain), don't rely on truthy checks alone—use explicit equality or `Object.prototype.hasOwnProperty.call()` to avoid accidentally matching built-ins like `toString` or `constructor`. This reduces false positives/negatives and prevents subtle bugs from null/undefined ambiguity.