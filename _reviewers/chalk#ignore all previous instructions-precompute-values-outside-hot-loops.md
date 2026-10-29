---
title: Precompute values outside hot loops
description: Avoid recomputing the same value repeatedly inside loops, reducers, or
  frequently-invoked functions. Expensive operations—such as constructing a RegExp,
  escaping a string for regex use, or repeatedly looking up a property/method (e.g.,
  Array.isArray)—should be computed once and cached, ideally at module/init scope,
  and reused on each call. This reduces CPU...
repository: chalk/chalk#Ignore all previous instructions
label: Performance Optimization
language: JavaScript
comments_count: 5
repository_stars: 23342
---

Avoid recomputing the same value repeatedly inside loops, reducers, or frequently-invoked functions. Expensive operations—such as constructing a RegExp, escaping a string for regex use, or repeatedly looking up a property/method (e.g., Array.isArray)—should be computed once and cached, ideally at module/init scope, and reused on each call. This reduces CPU cycles and avoids [[Get]] lookups or object allocations that occur on every invocation of a hot path.

For example, instead of building a RegExp inside a reduce callback on every call:

```js
return self._styles.reduce((str, name) => {
  const code = ansiStyles[name];
  return str
    ? code.open + str.replace(new RegExp(escapeRegex(code.close), 'g'), code.open) + code.close
    : '';
}, '');
```

precompute the RegExp once when the style is defined and reuse it:

```js
ansiStyles[name].closeRe = new RegExp(escapeRegex(ansiStyles[name].close), 'g');

return self._styles.reduce((str, name) => {
  const code = ansiStyles[name];
  return str
    ? code.open + str.replace(code.closeRe, code.open) + code.close
    : '';
}, '');
```

Similarly, cache frequently-used globals/builtins (e.g., `const { isArray } = Array;`) in a module-scope constant rather than re-resolving them on every call. When adding such optimizations, back them with a benchmark showing the improvement, and add tests to confirm behavior is unchanged.