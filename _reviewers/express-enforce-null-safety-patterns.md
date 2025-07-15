---
title: Enforce null safety patterns
description: 'Implement comprehensive null safety patterns to prevent runtime errors
  and ensure predictable behavior. Follow these guidelines:


  1. Use explicit null/undefined checks instead of loose comparisons:'
repository: expressjs/express
label: Null Handling
language: JavaScript
comments_count: 8
repository_stars: 67300
---

Implement comprehensive null safety patterns to prevent runtime errors and ensure predictable behavior. Follow these guidelines:

1. Use explicit null/undefined checks instead of loose comparisons:
```javascript
// Good
if (value === undefined || value === null) {
  // handle null case
}

// Avoid
if (!value) // Could match 0, '', false
if (typeof value === 'undefined') // Doesn't catch null
```

2. Never mutate input parameters or objects:
```javascript
// Good
function process(options) {
  const opts = { ...options }; // Create new object
  opts.value = opts.value || defaultValue;
  return opts;
}

// Avoid
function process(options) {
  options.value = options.value || defaultValue; // Mutates input
  return options;
}
```

3. Use Object.create(null) for clean object instances without prototype chain:
```javascript
// Good
const cleanObject = Object.create(null);

// Avoid
const dirtyObject = {}; // Inherits from Object.prototype
```

4. Implement strict type checking for boolean options:
```javascript
// Good
if (typeof options.flag !== 'boolean') {
  throw new TypeError('flag must be boolean');
}

// Avoid
if (options.flag) // Allows non-boolean values
```

This pattern prevents common null-related bugs, ensures type safety, and maintains immutability principles.