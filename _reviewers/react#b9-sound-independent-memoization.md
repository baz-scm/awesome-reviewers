---
title: Sound independent memoization
description: 'When caching/memoizing computed values, establish *sound memoization
  boundaries*: (1) memoize independently when the consumer cannot mutate the value,
  and (2) ensure macro inputs are transitively memoized so dependent expressions remain
  stable.'
repository: facebook/react#b9
label: Caching
language: Markdown
comments_count: 3
repository_stars: 251891
---

When caching/memoizing computed values, establish *sound memoization boundaries*: (1) memoize independently when the consumer cannot mutate the value, and (2) ensure macro inputs are transitively memoized so dependent expressions remain stable.

Apply this rule:
- Independent memoization: If you can prove a consumer function/macro treats a value as read-only (doesn’t mutate it), you may cache the produced value based only on its true dependencies—don’t tie its memo lifetime to unrelated surrounding cached slots.
- Transitive memoization for macros: For any custom macro, memoize its arguments *transitively* (i.e., memoize any sub-expressions required for the macro’s correctness/stability), not just a subset of cases.

Example (independent memoization when consumer doesn’t mutate input):
```js
// Instead of assuming `fn` might mutate `arr`, memoize `arr` by its real input.
let t1;
if ($[0] !== b) {
  t1 = makeArray(b);
  $[0] = b;
  $[1] = t1;
} else {
  t1 = $[1];
}
const arr = t1;
fn(arr); // safe to cache `arr` independently if `fn` is non-mutating
```

Example (transitive memoization for custom macro arguments):
```js
// Ensure macro arguments are memoized transitively, not only partially.
t0 = idx(props, (_) => _.group.label);
```

Result: fewer incorrect cache invalidations (by avoiding unnecessary coupling) and fewer correctness issues (by ensuring macro argument stability).