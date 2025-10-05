---
title: explicit error type handling
description: Handle errors with explicit type checking and intentional decisions rather
  than generic catch-all approaches. This improves error handling precision and makes
  error recovery logic clearer.
repository: TanStack/router
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 11590
---

Handle errors with explicit type checking and intentional decisions rather than generic catch-all approaches. This improves error handling precision and makes error recovery logic clearer.

Key practices:
- Check for specific error types and names rather than generic Error catching
- Use precise string matching (startsWith) instead of loose matching (includes) for error identification
- Be explicit about when errors should be silently handled vs when they should propagate
- Provide sensible defaults while allowing type flexibility when needed

Example of explicit error type checking:
```typescript
// Good: Explicit check for specific error type
if (e instanceof DOMException && e.name === 'AbortError') {
  // Handle as normal control flow
  return handleAbortError()
}

// Good: Specific error detection
function isRecoverableError(error: unknown): boolean {
  if (error instanceof Error) {
    return error.message.startsWith(`${RECOVERABLE_ERROR}: `)
  }
  return false
}

// Good: Explicit about silent error handling with documentation
try {
  const context = defaultTransformer.parse(serializedContext)
  return { context, data: formData }
} catch (e) {
  // Intentionally return fallback when context parsing fails
  // to allow request processing to continue
  return { data: formData }
}
```

This approach prevents unexpected error swallowing, makes error handling intentions clear to other developers, and enables more precise error recovery strategies.