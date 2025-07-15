---
title: " Preserve error context"
description: "When handling errors, always ensure the original error context is preserved and properly surfaced. Error information should never be silently swallowed in try/catch blocks, as this makes debugging extremely difficult and can lead to unexpected system behavior."
repository: "fastify/fastify"
label: "Error Handling"
language: "JavaScript"
comments_count: 5
repository_stars: 34000
---

When handling errors, always ensure the original error context is preserved and properly surfaced. Error information should never be silently swallowed in try/catch blocks, as this makes debugging extremely difficult and can lead to unexpected system behavior.

There are two recommended approaches to preserving error context:

1. Use the standard `error.cause` property to maintain error chains:

```javascript
try {
  // Original operation
  const result = func(error, reply.request, reply);
  // Process result...
} catch (err) {
  // Preserve original error context
  if (!Object.prototype.hasOwnProperty.call(err, 'cause')) {
    err.cause = error; // Link the original error as the cause
  } else {
    // Log when unable to set cause to avoid losing context
    logger.warn({
      err: error,
      parentError: err,
      message: 'Original error cannot be linked as cause'
    });
  }
  
  // Propagate the error with context preserved
  throw err;
}
```

2. In asynchronous code, ensure proper promise rejection handling:

```javascript
// BAD: Double resolution if error occurs
sget(options, (err, response, body) => {
  if (err) reject(err)
  resolve({ response, body }) // Still runs after reject!
})

// GOOD: Return after rejection to prevent double resolution
sget(options, (err, response, body) => {
  if (err) {
    reject(err)
    return // Important! Prevents executing the resolve
  }
  resolve({ response, body })
})
```

Remember that proper error handling includes validation of your error conditions themselves. Be careful with falsy checks that might incorrectly handle empty strings or zero values as error conditions.