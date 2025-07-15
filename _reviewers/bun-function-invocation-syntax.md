---
title: Function invocation syntax
description: Use the appropriate invocation syntax for functions based on their intended
  usage. Regular functions should be called directly without the `new` keyword, while
  constructor functions (typically capitalized) should be instantiated with `new`.
repository: oven-sh/bun
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 79093
---

Use the appropriate invocation syntax for functions based on their intended usage. Regular functions should be called directly without the `new` keyword, while constructor functions (typically capitalized) should be instantiated with `new`.

Incorrect:
```javascript
// Using constructor syntax with a regular function
const context2 = new vm.createContext(context);
```

Correct:
```javascript
// Calling a regular function properly
const context2 = vm.createContext(context);

// Using constructor syntax with an actual constructor
const myDate = new Date();
```

This distinction is important for code correctness and readability. Using `new` with a non-constructor function can lead to unexpected behavior, while omitting `new` when required can cause the function to execute in the global context instead of creating a new object instance.