---
title: Independent Memoization Rules
description: 'Cache derived values independently to improve performance, but only
  when correctness is guaranteed.


  Apply this rule:

  1) Safe-to-cache condition: You may memoize a derived value (e.g., `arr`, JSX used
  in `fbt.param`) independently if you can rely on the fact that any downstream call
  using it will not mutate that value. If a function *might* mutate its...'
repository: facebook/react#b11
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251894
---

Cache derived values independently to improve performance, but only when correctness is guaranteed.

Apply this rule:
1) Safe-to-cache condition: You may memoize a derived value (e.g., `arr`, JSX used in `fbt.param`) independently if you can rely on the fact that any downstream call using it will not mutate that value. If a function *might* mutate its argument, treat the value as invalidated and avoid independent memoization.
2) Dependency granularity: Use cache keys that reflect the *exact* inputs for the derived value. Recompute the derived value only when its specific dependencies change, not when unrelated values change.

Example (safe independent memoization):
```js
function Foo(b, fnFactory) {
  const fn = fnFactory(); // known: fn does not mutate its argument

  let t1;
  // Cache `makeArray(b)` independently from other values
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

Example (fine-grained caching for param content):
```js
function Component(props) {
  const $ = _c(4);

  let t2;
  const t1 = identity(props.text);
  if ($[2] !== t1) {
    t2 = <>{t1}</>;
    $[2] = t1;
    $[3] = t2;
  } else {
    t2 = $[3];
  }

  // Use cached param value
  return fbt._param('some label', t2);
}
```

If you can’t establish the “no mutation of argument” property or you can’t precisely name dependencies for the derived value, fall back to recomputation or coarser caching keys to maintain correctness.