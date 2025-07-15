---
title: "Complete error handling chain"
description: "Implement comprehensive error handling throughout the codebase by ensuring all error scenarios are properly caught, typed, and propagated. This includes always including catch blocks for async operations, properly typing and propagating error information, using standardized error codes, and ensuring error callbacks receive and handle error parameters."
repository: "axios/axios"
label: "Error Handling"
language: "JavaScript"
comments_count: 5
repository_stars: 107000
---

Implement comprehensive error handling throughout the codebase by ensuring all error scenarios are properly caught, typed, and propagated. This includes:

1. Always include catch blocks for async operations
2. Properly type and propagate error information
3. Use standardized error codes for consistent error handling
4. Ensure error callbacks receive and handle error parameters

Example:
```javascript
// Bad
import(modulePath)
  .then(module => {
    module.default(req, res);
  });

// Good
import(modulePath)
  .then(module => {
    module.default(req, res);
  })
  .catch(error => {
    // Properly typed error with standardized code
    const err = new Error('Module load failed');
    err.code = 'EMODLOAD';
    err.cause = error;
    errorHandler(err);
  });

// For error callbacks
service.use(
  (config) => { /* ... */ },
  (error) => {
    // Properly handle error parameter
    errorLogger(error);
    throw error; // Propagate if needed
  }
);
```