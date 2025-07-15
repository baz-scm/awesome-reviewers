---
title: "Proper Error Handling in Axios TypeScript Code"
description: "As a code reviewer, it is important to ensure that Axios-based TypeScript code properly handles and propagates errors. Key recommendations include using console.error() instead of console.log() when logging errors, preserving the full error object rather than just the error message, and following established Axios error handling patterns."
repository: "axios/axios"
label: "Axios"
language: "TypeScript"
comments_count: 4
repository_stars: 107000
---

As a code reviewer, it is important to ensure that Axios-based TypeScript code properly handles and propagates errors. Key recommendations:

1. Use `console.error()` instead of `console.log()` when logging errors to maintain complete error context.
2. When handling Axios promise rejections, always preserve the full error object rather than just the error message. This provides downstream error handlers with the necessary information for debugging.
3. Follow established Axios error handling patterns, such as using `.catch()` blocks in promise chains to centralize error logging and potential recovery logic.
4. Ensure consistent error handling approaches are used throughout the codebase, such as always including the full error object when logging or rejecting promises.

Example of proper Axios error handling in TypeScript:

```typescript
// In Axios interceptors, preserve the full error object
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error(error);
    return Promise.reject(error);
  }
);

// In promise chains, use consistent error handling
axios.get('/user?ID=12345')
  .then((response) => {
    // handle success
    console.log(response.data);
  })
  .catch((error) => {
    console.error(error);
    // Consider error recovery or propagation needs
  })
  .finally(() => {
    // always executed
  });
```

This approach enables better debugging, maintains backward compatibility, and follows established Axios error handling conventions.