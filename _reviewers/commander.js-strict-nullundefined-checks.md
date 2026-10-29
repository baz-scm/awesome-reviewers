---
title: Strict null/undefined checks
description: 'Use explicit, strict equality (`===`/`!==`) when checking for `null`
  or `undefined` instead of loose equality (`!=`/`==`) or `typeof` comparisons, which
  can mask bugs or be unnecessarily verbose. Be especially careful with `typeof value
  === ''object''` checks: since `typeof null === ''object''`, always add an explicit
  `value !== null` guard before accessing...'
repository: tj/commander.js
label: Null Handling
language: JavaScript
comments_count: 4
repository_stars: 28444
---

Use explicit, strict equality (`===`/`!==`) when checking for `null` or `undefined` instead of loose equality (`!=`/`==`) or `typeof` comparisons, which can mask bugs or be unnecessarily verbose. Be especially careful with `typeof value === 'object'` checks: since `typeof null === 'object'`, always add an explicit `value !== null` guard before accessing properties or calling methods like `Object.getPrototypeOf(value)`, otherwise the code will throw on null inputs.

```js
// Bad: crashes when value is null
if (typeof value === 'object' && Object.getPrototypeOf(value).toString !== Object.prototype.toString) { ... }

// Good: guard against null explicitly
if (typeof value === 'object' && value !== null && typeof value.toString === 'function' && value.toString !== Object.prototype.toString) { ... }
```

Also adopt a consistent convention for initializing "empty" properties: use `null` to represent an explicitly unset value, and reserve `undefined` only for properties that are lazily initialized (with a comment explaining why). Avoid relying on truthy/falsy checks against object properties that may collide with inherited built-ins (e.g. `toString`); prefer strict comparisons or `Object.prototype.hasOwnProperty.call(obj, key)` to confirm a value was actually set, rather than `typeof obj[key] !== 'undefined'`.