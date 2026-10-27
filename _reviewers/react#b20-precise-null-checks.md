---
title: Precise null checks
description: 'Make null/undefined handling explicit and intentional rather than defensive
  guesswork:


  1. Prefer strict comparisons (`=== null`, `!== null`) over loose ones (`== null`,
  `!= null`) when the type is known to only be `null` (not `undefined`), so the check
  communicates exactly what''s being tested. Reserve `== null` for cases where a value
  can genuinely be...'
repository: facebook/react#b20
label: Null Handling
language: JavaScript
comments_count: 9
repository_stars: 251895
---

Make null/undefined handling explicit and intentional rather than defensive guesswork:

1. Prefer strict comparisons (`=== null`, `!== null`) over loose ones (`== null`, `!= null`) when the type is known to only be `null` (not `undefined`), so the check communicates exactly what's being tested. Reserve `== null` for cases where a value can genuinely be either `null` or `undefined` and you intend to treat both the same way.

2. Keep type annotations accurate: mark a parameter/field as nullable (`?Type` or `Type | null`) only when `null`/`undefined` is actually a valid runtime value; drop the nullable qualifier once the code guarantees the value can't be null (e.g. after a runtime guard), instead of carrying `| null` through unnecessarily.
```js
// Bad: parentObject can never be null here, runtime guard already ensures it
function walk(response, value, parentObject: Object | null, key) {}

// Good
function walk(response, value, parentObject: Object, key) {}
```

3. Don't add optional chaining (`?.`) or extra null checks "just in case" when the static types already guarantee non-null. If the types are wrong, fix the types—don't paper over it with `?.`, since that can silently produce incorrect results instead of surfacing the real bug:
```js
// Bad: masks a type error and may silently compute the wrong result
if (prevHook?.subHooks?.length > 0 && nextHook?.subHooks?.length > 0) {}

// Good: trust the type, let it throw if the assumption is ever violated
if (prevHook.subHooks?.length > 0 && nextHook.subHooks?.length > 0) {}
```

4. Double-check the logic of combined null-safety expressions (`&&`, `!`, `?.`)—negating an optional-chained expression is not equivalent to negating a `&&`-guarded one:
```js
// Bug: when runtimeSourceURL is undefined, this is falsy (wrong)
runtimeSourceURL && !runtimeSourceURL.startsWith('<anonymous')
// Correct: undefined is treated as "doesn't start with"
!runtimeSourceURL?.startsWith('<anonymous')
```

5. When a null/undefined check could hide a real bug (an unexpected null that should never occur), prefer throwing/invariant over silently no-op'ing, unless the no-op is an intentional, documented behavior (e.g., ignoring calls on an unmounted instance). If you must cast away a null unsafely as a stopgap, mark it with `$FlowFixMe` (or equivalent) to flag it as technical debt rather than leaving an implicit, unexplained cast.