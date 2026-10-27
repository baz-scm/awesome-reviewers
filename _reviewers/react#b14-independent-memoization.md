---
title: Independent memoization
description: When you have a derived value whose inputs are stable and whose producer/helper
  does not mutate external state or its arguments, you can cache (memoize) it independently
  instead of tying recomputation to a larger expression.
repository: facebook/react#b14
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251893
---

When you have a derived value whose inputs are stable and whose producer/helper does not mutate external state or its arguments, you can cache (memoize) it independently instead of tying recomputation to a larger expression.

How to apply:
1) Verify safety: ensure the function/helper is pure with respect to its arguments (no argument mutation, no hidden side effects that would make cached results stale).
2) Compute cache scope by direct dependencies only: memoize the smallest subexpression possible whose output depends only on known variables.
3) Reuse the cached value in the parent expression/helper call.

Example pattern (memoize an intermediate, then reuse):
```js
function Component(props) {
  const $ = _c(2);

  let t1;
  // Cache an independently derived value based only on direct deps
  if ($[0] !== props.text) {
    const derived = identity(props.text);
    $[0] = props.text;
    $[1] = derived;
    t1 = derived;
  } else {
    t1 = $[1];
  }

  // Reuse cached derived value inside a compound call
  return fbt._("...", [
    fbt._param("item author", t1),
  ]);
}
```

Result: fewer recomputations, smaller invalidation surfaces, and more predictable caching behavior.