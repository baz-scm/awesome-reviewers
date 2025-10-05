---
title: Intentional async usage
description: Be deliberate about when to use the `async` keyword and `await` expressions.
  Making a function `async` changes its behavior - it will always return a Promise,
  even for early returns. This can break conditional logic that checks for synchronous
  vs asynchronous behavior.
repository: TanStack/router
label: Concurrency
language: TypeScript
comments_count: 2
repository_stars: 11590
---

Be deliberate about when to use the `async` keyword and `await` expressions. Making a function `async` changes its behavior - it will always return a Promise, even for early returns. This can break conditional logic that checks for synchronous vs asynchronous behavior.

Consider these patterns:
- Use `async` only when you actually need to `await` something
- For functions with early returns that should be synchronous, return Promise.all() or similar constructs directly instead of using async/await
- Remove unnecessary `await` keywords that don't add value

Example from the codebase:
```typescript
// Avoid: Always returns Promise due to async, breaks early return logic
const executeHead = async () => {
  if (!match) {
    return // Still returns Promise<undefined>
  }
  // ... rest of function
}

// Prefer: Early returns are synchronous, later returns are Promise
const executeHead = () => {
  if (!match) {
    return // Returns undefined directly
  }
  return Promise.all([
    // async operations here
  ])
}
```

This approach preserves the ability to use patterns like `if('then' in result)` to detect whether a function returned a Promise or a synchronous value.