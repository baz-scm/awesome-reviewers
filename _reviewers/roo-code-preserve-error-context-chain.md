---
title: Preserve error context chain
description: When catching and re-throwing errors, always preserve the original error
  context using the `cause` option of the Error constructor. This maintains the complete
  error chain for debugging and ensures no critical information is lost when translating
  errors between layers.
repository: RooCodeInc/Roo-Code
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 17288
---

When catching and re-throwing errors, always preserve the original error context using the `cause` option of the Error constructor. This maintains the complete error chain for debugging and ensures no critical information is lost when translating errors between layers.

Instead of:
```typescript
try {
  await deletePoints(filePaths)
} catch (error) {
  throw new Error(`Failed to delete points: ${error.message}`)
}
```

Use:
```typescript
try {
  await deletePoints(filePaths)
} catch (error) {
  throw new Error(
    `Failed to delete points: ${error instanceof Error ? error.message : String(error)}`,
    { cause: error }
  )
}
```

This practice:
- Preserves the original error's stack trace and type information
- Maintains the full error chain for debugging
- Allows adding context at each layer while keeping the root cause
- Enables proper error tracking and logging
- Facilitates better error handling decisions in upper layers

When handling errors across system boundaries (e.g., API calls, file operations), this becomes especially important as it helps track down issues through multiple abstraction layers.