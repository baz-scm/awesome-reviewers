---
title: Clear array operations
description: When working with arrays, prioritize clarity and explicitness over terse
  or clever constructs. For array membership checks, use `array.indexOf(item) ===
  -1` rather than less obvious expressions like `!~array.indexOf(item)` or `array.indexOf(item)
  < 0`. This improves readability and makes code intent immediately clear to other
  developers.
repository: expressjs/express
label: Algorithms
language: JavaScript
comments_count: 2
repository_stars: 67300
---

When working with arrays, prioritize clarity and explicitness over terse or clever constructs. For array membership checks, use `array.indexOf(item) === -1` rather than less obvious expressions like `!~array.indexOf(item)` or `array.indexOf(item) < 0`. This improves readability and makes code intent immediately clear to other developers.

Be cautious with array manipulation methods that can cause unexpected behavior. The `.concat()` method can flatten arrays in unexpected ways:

```js
// Potentially problematic:
[key].concat(fns)  // Will flatten if fns contains arrays

// More predictable alternatives:
[key, ...fns]      // ES6 spread syntax preserves structure
[].concat([key], fns)  // More explicit nesting
```

These practices ensure that array operations behave predictably and their intention is clear to anyone reading the code, which is especially important for search and manipulation algorithms.