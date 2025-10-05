---
title: Clear contextual error messages
description: Error messages should be specific, contextually relevant, and provide
  actionable guidance to developers. Avoid generic or ambiguous error text that could
  apply to multiple scenarios.
repository: TanStack/router
label: Error Handling
language: TSX
comments_count: 2
repository_stars: 11590
---

Error messages should be specific, contextually relevant, and provide actionable guidance to developers. Avoid generic or ambiguous error text that could apply to multiple scenarios.

In tests, use distinct error messages for different components or scenarios so that test failures clearly indicate the expected outcome:

```tsx
const rootRoute = createRootRoute({
  errorComponent: () => <span>Rendering errorComp message</span>,
  component: () => {
    throw new Error('Throwing from route component')
  }
})
```

For runtime errors, provide context about where the error occurred and suggest specific solutions:

```tsx
// Instead of generic: "No match found while rendering useMatch()"
// Use contextual: "No match found for route '/' while rendering the '/about' route. Did you mean to pass '{ strict: false }' instead?"
```

This approach helps developers quickly identify the source of errors and understand how to resolve them, whether during development, testing, or debugging production issues.