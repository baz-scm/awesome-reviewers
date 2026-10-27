---
title: Precise null checks
description: Be deliberate about distinguishing `null`, `undefined`, and other falsy
  values, and keep null-checking style consistent with the surrounding code and the
  actual type contracts involved.
repository: facebook/react#b18
label: Null Handling
language: JavaScript
comments_count: 9
repository_stars: 251889
---

Be deliberate about distinguishing `null`, `undefined`, and other falsy values, and keep null-checking style consistent with the surrounding code and the actual type contracts involved.

- Match the check to the real type. If a field can only be `null` (not `undefined`), compare with `=== null`/`!== null` rather than `== null` or the reverse; conflating the two is a sign of type confusion (e.g. comparing `_debugEndTime === null` when the field is typed as `void`/`undefined`) and should be fixed at the type level, not papered over.
- Prefer strict equality (`=== null` / `!== null`) for consistency with existing checks in the same function/file, unless you intentionally want to cover both `null` and `undefined`, in which case use `== null` explicitly and consistently rather than mixing styles.
- Don't add defensive optional chaining (`?.`) or loose guards for values that the type system guarantees are non-null. If the types say a value can't be null/undefined, trust them — let an invalid state throw so the bug is caught early, instead of silently working around it and risking incorrect behavior.
- When an early return/guard exists for a condition that produces a null value (e.g. a ref that's only null under specific conditions), check that same originating condition instead of just checking the resulting value is null; a null value outside that condition should be a loud bug, not a silent no-op.
- Always explicitly assign `null`/reset nullable state in all code paths, even when "nothing to set" — leaving a stale previous value can cause incorrect reads later.
- Before calling methods on globals or external APIs that may be unavailable in some environments (e.g. `navigator` in non-browser contexts like Electron), check for existence first instead of assuming they're always defined.
- When using optional chaining or `&&` guards for null-safety, double-check the boolean logic — negating an already-safe optional-chain expression can silently invert intended behavior.

Example of matching the check to type semantics and avoiding unnecessary type casts:
```js
// Bad: internal-only state typed loosely, then cast away with `any`
let signal: void | AbortSignal;
store = (null: any);

// Good: use the real nullable type, and flag unavoidable casts for follow-up
let signal: null | AbortSignal = null;
// $FlowFixMe[incompatible-type] - cleanup tracked in #1234
store = (null: any);
```