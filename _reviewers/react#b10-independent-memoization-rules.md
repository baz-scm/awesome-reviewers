---
title: Independent memoization rules
description: When caching/memoizing derived values, allow **independent caching**
  only if you can establish that downstream computations won’t mutate those cached
  values.
repository: facebook/react#b10
label: Caching
language: Markdown
comments_count: 2
repository_stars: 251894
---

When caching/memoizing derived values, allow **independent caching** only if you can establish that downstream computations won’t mutate those cached values.

Apply this as a checklist:
- **Purity / no mutation proof:** If a later call (e.g., a function value) could mutate the computed value, you must not cache independently. If you can prove it won’t mutate its argument (or otherwise affect it), you may cache the derived value separately.
- **Dependency isolation:** Memoize based solely on the direct inputs of the derived value (e.g., memoize `makeArray(b)` based on `b`, not on unrelated later computations).
- **Reusable cache slots:** If the compiler/runtime already tracks cached temporaries (`$[...]`), reuse them to avoid recomputation across paths.

Example pattern (independent memoization after proving non-mutation):
```js
function Foo(t0, b, fn) {
  // If `fn` does not mutate its argument, memoize `arr` independently from `fn`.
  let t1;
  if ($[0] !== b) {
    t1 = makeArray(b);
    $[0] = b;
    $[1] = t1;
  } else {
    t1 = $[1];
  }
  const arr = t1;
  fn(arr);
}
```

Similarly, for parameter-like values that are computed from their inputs, treat them as their own memoization units (e.g., `fbt.param` values can be cached independently from other surrounding expressions) as long as their dependencies are the only inputs that determine the result.