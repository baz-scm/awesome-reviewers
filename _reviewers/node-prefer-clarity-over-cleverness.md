---
title: Prefer clarity over cleverness
description: Write code that prioritizes readability and maintainability over cleverness
  or excessive optimization. Avoid overly clever techniques that might confuse other
  developers or make the code harder to maintain.
repository: nodejs/node
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 112178
---

Write code that prioritizes readability and maintainability over cleverness or excessive optimization. Avoid overly clever techniques that might confuse other developers or make the code harder to maintain.

Key principles:
- Use straightforward, explicit code over clever shortcuts
- Avoid unnecessary processing like creating arrays just to join them into strings
- Eliminate redundant conditionals and unnecessary checks
- Consider compiler optimizations when extracting or inlining functions
- Use consistent function styles (regular vs. arrow) based on their purpose

Example - Instead of this clever approach:
```javascript
const handleTypes = ['TCP', 'TTY', 'UDP', 'FILE', 'PIPE', 'UNKNOWN'];
setOwnProperty(handleTypes, -1, null);
// Later using handleTypes[someIndex]
```

Prefer this more explicit approach:
```javascript
const handleTypes = ['TCP', 'TTY', 'UDP', 'FILE', 'PIPE', 'UNKNOWN'];

function getHandleType(type) {
  return type >= 0 && type < handleTypes.length ? handleTypes[type] : null;
}
```

Similarly, prefer direct string creation over array joining for static content:
```javascript
// Instead of:
const message = [
  'Error: This file cannot be parsed as either CommonJS or ES Module.',
  '- CommonJS error: await is only valid in async functions.',
  '- ES Module error: require is not defined in ES module scope.'
].join('\n');

// Prefer:
const message = 'Error: This file cannot be parsed as either CommonJS or ES Module. ' +
  'CommonJS error: await is only valid in async functions. ' +
  'ES Module error: require is not defined in ES module scope.';
```

When functions are called multiple times, consider the performance implications of inlining vs. extracting. Unnecessary function extraction can hinder compiler optimizations in hot paths.