---
title: Independent Memoization
description: Cache values independently when (a) the value is derived solely from
  a stable set of inputs and (b) the consumer will not mutate it. Don’t force broader
  cache entries to own sub-value recomputation—split memoization so each derived value
  has its own dependency boundary.
repository: facebook/react#b17
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251891
---

Cache values independently when (a) the value is derived solely from a stable set of inputs and (b) the consumer will not mutate it. Don’t force broader cache entries to own sub-value recomputation—split memoization so each derived value has its own dependency boundary.

Apply by:
- Confirm non-mutation/purity: if a function doesn’t mutate its arguments, you can memoize the argument/value based on its inputs without assuming it must stay synchronized with the outer cache.
- Split dependency boundaries: for composed calls (e.g., param-based composition), compute each param’s value separately and reuse it across renders until that param’s inputs change.

Pattern (conceptual):
```js
// Inputs: b, myVar
let t1;
if ($[0] !== b) {
  t1 = makeArray(b); // memoize derived value from b only
  $[0] = b;
  $[1] = t1;
} else {
  t1 = $[1];
}
fn(t1); // safe if fn does not mutate its argument

// For param-like composition: memoize the param value from its own inputs
let t2;
if ($[2] !== name) {
  t2 = <Text type="h4">{name}</Text>;
  $[2] = name;
  $[3] = t2;
} else {
  t2 = $[3];
}
fbt._param("item author", t2);
```
This improves cache performance by reducing unnecessary recomputation and avoids incorrect coupling between unrelated cached regions.