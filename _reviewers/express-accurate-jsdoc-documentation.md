---
title: Accurate JSDoc documentation
description: Always ensure JSDoc comments accurately reflect the actual code implementation.
  Parameter types, optionality, and function behavior must be precisely documented
  to prevent confusion and bugs.
repository: expressjs/express
label: Documentation
language: JavaScript
comments_count: 2
repository_stars: 67300
---

Always ensure JSDoc comments accurately reflect the actual code implementation. Parameter types, optionality, and function behavior must be precisely documented to prevent confusion and bugs.

When documenting parameters:
- Match the exact types accepted by the function
- Indicate optional parameters appropriately
- Verify documentation when code changes

For example, if a function accepts multiple types or optional parameters:

```javascript
/**
 * Process user input
 *
 * @param {String|Array} input - The input to process
 * @param {Object} [options] - Optional configuration object
 * @return {Boolean} Whether processing succeeded
 */
function process(input, options) {
  // implementation
}
```

Incorrect or outdated JSDoc can mislead developers and lead to runtime errors. Always review JSDoc comments when changing function signatures or behavior to ensure documentation and implementation remain synchronized.