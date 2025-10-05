---
title: break complex expressions
description: Break down complex boolean expressions and conditions into well-named
  intermediate variables to improve code readability and maintainability. Instead
  of writing dense one-liners, use descriptive variable names that clearly communicate
  the intent of each condition.
repository: TanStack/router
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 11590
---

Break down complex boolean expressions and conditions into well-named intermediate variables to improve code readability and maintainability. Instead of writing dense one-liners, use descriptive variable names that clearly communicate the intent of each condition.

For unused parameters in catch blocks or function signatures, prefix them with an underscore to maintain access for debugging while silencing linter warnings.

Example of improving a complex boolean expression:
```ts
// Instead of this complex one-liner:
return !(d.status !== 'error' && Date.now() - d.updatedAt < gcTime)

// Break it down into descriptive variables:
const isError = d.status === 'error'
const isElapsed = Date.now() - d.updatedAt >= gcTime
return isError && isElapsed
```

Example of proper unused parameter handling:
```ts
// Instead of empty catch:
} catch {

// Use underscore prefix for potential debugging access:
} catch (_err) {
  // Can still access _err for console.log during development
}
```

This approach makes code self-documenting and easier to understand, debug, and maintain.