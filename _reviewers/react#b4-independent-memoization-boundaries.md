---
title: Independent memoization boundaries
description: 'Cache derived values independently whenever you can prove they are safe
  from side effects and only depend on specific inputs.


  Apply this when:

  - A function call is pure (e.g., does not mutate its arguments) or otherwise doesn’t
  introduce observable side effects that would change a cached value.'
repository: facebook/react#b4
label: Caching
language: Markdown
comments_count: 2
repository_stars: 251885
---

Cache derived values independently whenever you can prove they are safe from side effects and only depend on specific inputs.

Apply this when:
- A function call is pure (e.g., does not mutate its arguments) or otherwise doesn’t introduce observable side effects that would change a cached value.
- A compound expression passes subvalues as arguments (e.g., template/translation params); each subvalue can be memoized against its own dependencies.

Consequence: increase memoization granularity so unrelated changes don’t force recomputation.

Example (pattern):
```js
// Instead of assuming the callee might affect the argument,
// cache the argument based solely on its true inputs.

let t;
if ($[0] !== b) {
  t = makeArray(b);
  $[0] = b;
  $[1] = t;
} else {
  t = $[1];
}

fn(t); // fn is known not to mutate its argument

// For compound params, memoize independent subexpressions:
let text;
if ($[4] !== name) {
  text = <Text type="h4">{name}</Text>;
  $[4] = name;
  $[5] = text;
} else {
  text = $[5];
}

fbt._param("item author", text);
```

Use this as a checklist: (1) identify the smallest dependency set for the derived value, (2) confirm no side effects can invalidate that value, (3) memoize/reuse at that boundary, and (4) wire memoized subvalues into compound calls/params.