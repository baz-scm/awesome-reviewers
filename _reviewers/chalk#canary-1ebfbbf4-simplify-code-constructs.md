---
title: Simplify code constructs
description: 'Favor simple, idiomatic JavaScript over verbose custom logic. This improves
  readability and reduces the number of code paths to maintain.


  - Use early returns instead of nested or chained ternaries for conditional logic:'
repository: chalk/chalk#CANARY-1ebfbbf4
label: Code Style
language: JavaScript
comments_count: 5
repository_stars: 23342
---

Favor simple, idiomatic JavaScript over verbose custom logic. This improves readability and reduces the number of code paths to maintain.

- Use early returns instead of nested or chained ternaries for conditional logic:
  ```js
  // Avoid
  return chalk.enabled && str ? doSomething(str) : str;

  // Prefer
  if (!chalk.enabled || !str) {
      return str;
  }
  return doSomething(str);
  ```
- Rely on built-in methods instead of manual loops or extra dependencies when they accomplish the same result. For example, use `Array.prototype.join()` to concatenate arguments instead of a manual loop with index checks, and use `.toString()` instead of custom type-coercion branches:
  ```js
  // Avoid
  for (var i = 0, str = '', j = arguments.length; i < j; i++) {
      str += arguments[i];
      if (i < j - 1) str += ' ';
  }

  // Prefer
  var str = [].slice.call(arguments).join(' ');
  ```
- Avoid adding conditional branches or special-casing when the general code path already handles all cases correctly (e.g., `arguments` is always array-like, so don't special-case `arguments.length > 1`).
- Prefer concise built-in array/string operations (e.g., `Array.prototype.filter`) over pulling in small utility dependencies when a one-liner suffices, and use regex capture groups instead of manual string splicing when replacing patterns:
  ```js
  // Avoid
  out = exclude(out, style.slice(1));

  // Prefer
  const toExclude = style.slice(1);
  out = out.filter(x => x !== toExclude);
  ```

Before introducing a loop, extra dependency, or multiple conditional branches, check whether a built-in method or a simpler single code path already covers the requirement.</description>
</invoke>
