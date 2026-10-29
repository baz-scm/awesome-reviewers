---
title: Prefer built-in methods
description: 'When a standard language feature already does the job, use it instead
  of a manual or custom reimplementation — this is clearer, less error-prone, and
  easier to maintain. Examples observed in review:'
repository: tj/commander.js
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 28444
---

When a standard language feature already does the job, use it instead of a manual or custom reimplementation — this is clearer, less error-prone, and easier to maintain. Examples observed in review:
- Use `Array.isArray(x)` instead of a hand-rolled `isArray()` helper.
- Use `str.endsWith('...')` instead of `str.slice(-3) === '...'` plus a redundant length check.
- Use `str.startsWith('--no-')` instead of `flags.indexOf('--no-') !== -1`, since `indexOf` can match the substring anywhere, not just at the start.
- Use default function parameters instead of manually checking for `undefined`:
  ```js
  // instead of
  allowExcessArguments(allowExcess) {
    if (allowExcess === undefined) allowExcess = true;
    ...
  }
  // prefer
  allowExcessArguments(allowExcess = true) {
    ...
  }
  ```
- Use `Object.prototype.hasOwnProperty.call(obj, key)` instead of the `in` operator when you only want to check the object's own properties (the `in` operator also matches inherited properties).
- When adding case-insensitivity or other variants to a regex, prefer a targeted character class (e.g. `[eE]`) over a blanket `/i` flag, so the intent of what varies is explicit rather than silently affecting the whole pattern.

Before writing custom logic, check whether a native method or language feature already covers the case; it communicates intent more clearly to readers and avoids subtle bugs from incomplete reimplementations.