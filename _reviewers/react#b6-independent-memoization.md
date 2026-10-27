---
title: Independent memoization
description: 'Cache derived values independently when it’s safe and the dependency
  set is known.


  Apply this by:

  - Proving (or inferring from types/signature) that downstream functions do not mutate
  their input arguments.'
repository: facebook/react#b6
label: Caching
language: Markdown
comments_count: 2
repository_stars: 251888
---

Cache derived values independently when it’s safe and the dependency set is known.

Apply this by:
- Proving (or inferring from types/signature) that downstream functions do not mutate their input arguments.
- Memoizing the producer expression based only on the inputs it actually depends on.
- If a larger expression contains multiple parameter-like sub-values (e.g., fbt params, JSX fragments), cache each sub-value separately so only the changed dependency recomputes.

Example pattern (split memoization from the consumer):

```js
function Foo(t0) {
  const fn = fnFactory(); // known not to mutate its argument
  let t1;

  // Cache the produced value strictly by its real dependency
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

And for parameter-like values, cache sub-expressions independently:

```js
function Component(t0) {
  const $ = _c(6);
  const { name, data, icon } = t0;
  let t1;

  if ($[0] !== data || $[1] !== icon || $[2] !== name) {
    let t2;
    if ($[4] !== name) {
      t2 = <Text type="h4">{name}</Text>;
      $[4] = name;
      $[5] = t2;
    } else {
      t2 = $[5];
    }

    t1 = (
      <Text type="body4">
        {fbt._("{item author}{icon}{=m2}", [fbt._param("item author", t2)])}
      </Text>
    );
  }
}
```

This reduces unnecessary recomputation and avoids incorrect cache coupling when mutation is not possible and dependencies are precise.