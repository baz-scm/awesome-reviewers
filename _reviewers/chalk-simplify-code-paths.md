---
title: Simplify code paths
description: 'Favor simple, idiomatic constructs over verbose or redundant logic.
  Specifically:


  - Avoid unnecessary conditional branches or special-casing when the same built-in
  method can handle all cases uniformly. For example, instead of checking `arguments.length
  > 1` and manually concatenating with a loop, just convert `arguments` to an array
  and call `.join('' '')`...'
repository: chalk/chalk
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 23342
---

Favor simple, idiomatic constructs over verbose or redundant logic. Specifically:

- Avoid unnecessary conditional branches or special-casing when the same built-in method can handle all cases uniformly. For example, instead of checking `arguments.length > 1` and manually concatenating with a loop, just convert `arguments` to an array and call `.join(' ')` on it — this works for any number of arguments and avoids extra code paths.

```js
// Avoid
if (arguments.length > 1) {
  for (var i = 0, str = '', j = arguments.length; i < j; i++) {
    str += arguments[i];
    if (i < j - 1) str += ' ';
  }
}

// Prefer
var str = [].slice.call(arguments).join(' ');
```

- Prefer built-in array/string methods (`join`, `filter`, `map`, `toString`) over manual loops or extra dependencies. For example, replace a custom "exclude" helper with a simple `filter`:

```js
// Avoid pulling in a dependency for this
out = exclude(out, style.slice(1));

// Prefer
const exclude = style.slice(1);
out = out.filter(x => x !== exclude);
```

- Replace chains of ternaries with early returns for readability:

```js
// Avoid
return chalk.enabled && str ? ... : str;

// Prefer
if (!chalk.enabled || !str) {
  return str;
}
```

- Remove unused parameters/variables; declare variables only where they are actually used.
- Use strict equality (`===`/`!==`) instead of loose equality (`==`/`!=`) to avoid implicit type coercion bugs.

Applying these guidelines keeps logic flat, reduces the number of code paths to test and maintain, and makes intent immediately clear to future readers.