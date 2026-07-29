---
title: Null-safe value handling
description: 'Make null/undefined (and “invalid/unknown”) states explicit and prevent
  them from flowing into non-null/non-optional operations.


  Apply these rules:

  1) Enforce compiler null safety: enable `strictNullChecks` so the typechecker blocks
  `x?.foo()`/`x.foo()` on `string | null`-like values.'
repository: earendil-works/pi
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 79783
---

Make null/undefined (and “invalid/unknown”) states explicit and prevent them from flowing into non-null/non-optional operations.

Apply these rules:
1) Enforce compiler null safety: enable `strictNullChecks` so the typechecker blocks `x?.foo()`/`x.foo()` on `string | null`-like values.
2) Guard before method calls: if a value can be `null`/`undefined`, check it before calling string/array methods.
3) Align conversion boundaries: parsing/normalization that accepts `unknown` must either:
   - return a valid, strongly-typed value, or
   - fail fast (throw) / return a discriminated union that forces handling.
   Never “parse may return undefined” but then pass the result into a function typed as “number only”.
4) Make fallback logic unambiguous: when using `?? default`, ensure `undefined` (missing support) and `false` (explicitly disabled) are treated differently.

Example (null guard + explicit fallback):
```ts
function getErrorPrefix(err: string | null | undefined) {
  if (!err) return null; // handles ''/null/undefined per your policy
  return err.startsWith('No API key found') ? err : null;
}

const constrainedStrict = supportsStrictMode
  ? resolveJsonSchemaStrictSampling(tool, true)
  : undefined; // explicit
const strict = constrainedStrict ?? defaultStrict; // only applies when constrainedStrict is undefined
```

This prevents unsafe member access, accidental propagation of `undefined`/invalid values across typed boundaries, and confusing fallback behavior.