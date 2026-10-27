---
title: Independent value memoization
description: 'Cache derived values on the smallest safe dependency set, and reuse
  those cached subresults inside larger expressions/params.


  Apply this when:

  - You can justify purity/no-mutation: if a function call cannot mutate its arguments,
  you may memoize the argument independently.'
repository: facebook/react#b5
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251886
---

Cache derived values on the smallest safe dependency set, and reuse those cached subresults inside larger expressions/params.

Apply this when:
- You can justify purity/no-mutation: if a function call cannot mutate its arguments, you may memoize the argument independently.
- You have nested values (e.g., JSX passed into formatting/param helpers): compute the nested value once into a cached temporary and pass the cached temporary onward.

Pattern (argument + nested param examples):
```js
// Argument memoization (safe when `fn` cannot mutate `arr`)
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

// Independent memoization of JSX used as a param value
let t2;
if ($[4] !== name) {
  t2 = <Text type="h4">{name}</Text>;
  $[4] = name;
  $[5] = t2;
} else {
  t2 = $[5];
}

// Reuse the memoized JSX value as the param argument
fbt._param("item author", t2);
```

Outcome: fewer recomputations and more precise cache invalidation—without changing behavior—by avoiding coupling the lifetime of a nested derived value to the broader expression that contains it.