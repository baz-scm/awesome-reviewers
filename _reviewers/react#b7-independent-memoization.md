---
title: Independent memoization
description: 'Memoize/cached subexpressions independently whenever passing a value
  into another function does not introduce mutation or coupling.


  Apply this standard:'
repository: facebook/react#b7
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251888
---

Memoize/cached subexpressions independently whenever passing a value into another function does not introduce mutation or coupling.

Apply this standard:
- Determine whether a callee can mutate its arguments (or otherwise create hidden dependencies). If it cannot (“doesn't mutate its argument”), you may cache derived inputs separately from the caller’s other cached values.
- For patterns like `fbt._param(...)` that take computed values (including JSX fragments/elements), treat each param value as independently memoizable: introduce a dedicated cached temp for the param’s value and reuse it when its inputs are unchanged.

Example (side-effect-free argument + independent caching):
```js
function Foo(props) {
  const $ = _c(2);

  let t1;
  if ($[0] !== props.b) {
    t1 = makeArray(props.b);
    $[0] = props.b;
    $[1] = t1;
  } else {
    t1 = $[1];
  }

  fn(t1);
}
```

Example (`fbt.param` JSX value independently memoized):
```js
function Component(t0) {
  const $ = _c(3);

  let t2;
  if ($[0] !== t0.name) {
    t2 = <Text type="h4">{t0.name}</Text>;
    $[0] = t0.name;
    $[1] = t2;
  } else {
    t2 = $[1];
  }

  return fbt._("{item author}{=m2}", [
    fbt._param("item author", t2),
  ]);
}
```