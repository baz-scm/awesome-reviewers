---
title: simplify error handling
description: Write concise and appropriate error handling code by avoiding unnecessary
  complexity and verbose constructions. Remove try-catch blocks when they serve no
  purpose, and use streamlined approaches for error message construction.
repository: menloresearch/jan
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 37620
---

Write concise and appropriate error handling code by avoiding unnecessary complexity and verbose constructions. Remove try-catch blocks when they serve no purpose, and use streamlined approaches for error message construction.

For example, instead of verbose error message handling:
```javascript
let errMessage = 'Unexpected Error'
if (err instanceof Error) {
  errMessage = err.message
}
toaster({
  title: 'Failed to get Hugging Face models',
  description: errMessage,
  type: 'error',
})
```

Use a more concise approach:
```javascript
toaster({
  title: 'Failed to get Hugging Face models',
  description: err instanceof Error ? err.message : 'Unexpected Error',
  type: 'error',
})
```

Similarly, avoid wrapping function calls in try-catch blocks when error handling isn't actually needed or when the function doesn't throw exceptions that require handling at that level.