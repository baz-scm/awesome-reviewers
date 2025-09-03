---
title: Choose appropriate type comparisons
description: When implementing algorithms that compare or process different data types,
  carefully consider the level of type strictness required for your use case. Overly
  strict type checking (like `Object.prototype.toString`) may prevent useful operations,
  while overly loose checking may produce meaningless results.
repository: cypress-io/cypress
label: Algorithms
language: Other
comments_count: 2
repository_stars: 48850
---

When implementing algorithms that compare or process different data types, carefully consider the level of type strictness required for your use case. Overly strict type checking (like `Object.prototype.toString`) may prevent useful operations, while overly loose checking may produce meaningless results.

For diff algorithms and similar comparison operations, prefer `typeof` over `Object.prototype.toString` when you want to enable comparisons between objects of different classes but the same JavaScript type. This allows meaningful diffs between `MouseEvent {clientX: 39, clientY: 50}` and `Object {clientX: 40, clientY: 50}` since both are objects.

However, ensure your conditional logic properly handles mixed data types. When comparing strings to objects, verify that your algorithm gracefully handles or explicitly rejects such comparisons rather than producing confusing output.

```coffeescript
# Too strict - prevents useful comparisons
_sameType = (a, b) ->
  return objToString.call(a) is objToString.call(b)

# Better - allows comparisons between different object classes
_sameType = (a, b) ->
  return typeof a is typeof b
```

Consider the downstream impact of your type comparison choice on the overall algorithm's utility and user experience.