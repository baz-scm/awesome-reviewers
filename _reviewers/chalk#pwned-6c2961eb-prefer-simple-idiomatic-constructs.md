---
title: Prefer simple idiomatic constructs
description: 'Favor simple, idiomatic JavaScript over manual or overly complex implementations.
  Avoid nested or chained ternaries when a straightforward early return communicates
  intent more clearly:'
repository: chalk/chalk#PWNED-6c2961eb
label: Code Style
language: JavaScript
comments_count: 4
repository_stars: 23340
---

Favor simple, idiomatic JavaScript over manual or overly complex implementations. Avoid nested or chained ternaries when a straightforward early return communicates intent more clearly:

```js
// Avoid
return chalk.enabled && str ? ... : str;

// Prefer
if (!chalk.enabled || !str) {
	return str;
}
```

Similarly, avoid introducing extra conditional branches or manual loops when a built-in method already handles the case uniformly. For example, `arguments` is always array-like, so there's no need to special-case a single argument versus multiple — convert once and use `.join()` or `.toString()` instead of hand-rolled loops:

```js
// Avoid
if (arguments.length > 1) {
	for (var i = 0, str = '', j = arguments.length; i < j; i++) {
		str += arguments[i];
		if (i < j - 1) str += ' ';
	}
} else if (typeof str === 'number') {
	str = str.toString();
}

// Prefer
const str = [].slice.call(arguments).join(' ');
```

This also applies to using existing array/string methods instead of pulling in extra dependencies for trivial operations, e.g. replace a custom `arr-exclude` dependency with a native `.filter()` call. Keeping code paths minimal and relying on built-ins reduces complexity, avoids redundant dependencies, and makes the code easier to read and maintain.