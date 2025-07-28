---
title: Enhance error message clarity
description: Error messages should be both specific about what went wrong and provide
  contextual information to help developers locate and fix the issue. Even in performance-critical
  or low-level APIs, basic validation with clear error messages is essential because
  "there's no easy way for the developer to get feedback on failures" otherwise.
repository: denoland/deno
label: Error Handling
language: JavaScript
comments_count: 2
repository_stars: 103714
---

Error messages should be both specific about what went wrong and provide contextual information to help developers locate and fix the issue. Even in performance-critical or low-level APIs, basic validation with clear error messages is essential because "there's no easy way for the developer to get feedback on failures" otherwise.

When validation fails, provide specific details about the invalid input and acceptable ranges or formats. Additionally, include contextual information such as stack traces to help developers identify the source of the error.

Example of good error messaging:
```javascript
// Specific error with details about what's wrong and what's expected
throw new RangeError(`The status provided (${status}) is not equal to 101 and outside the range [200, 599].`);

// Adding contextual information to warnings
console.warn(
  "Prototype access via __proto__ attempted; __proto__ is not implemented in Deno due to security reasons. Use Object.setPrototypeOf instead.",
  new Error().stack
);
```

This approach balances performance considerations with developer experience by providing minimal but meaningful validation and clear guidance on how to resolve issues.