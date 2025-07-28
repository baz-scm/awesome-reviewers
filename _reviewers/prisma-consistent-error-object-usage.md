---
title: consistent error object usage
description: Always use proper Error objects when throwing exceptions, maintain consistent
  error handling contracts, and ensure type safety in error scenarios. Avoid throwing
  primitive strings, mixing throw/return patterns, or unsafe type assertions on error
  objects.
repository: prisma/prisma
label: Error Handling
language: TypeScript
comments_count: 7
repository_stars: 42967
---

Always use proper Error objects when throwing exceptions, maintain consistent error handling contracts, and ensure type safety in error scenarios. Avoid throwing primitive strings, mixing throw/return patterns, or unsafe type assertions on error objects.

Key principles:
- Throw Error objects, not strings: Use `throw new Error('message')` instead of `throw 'message'`
- Maintain consistent function contracts: If a function signature suggests it returns `undefined` on failure, don't throw instead
- Use proper typing for error handling: Cast caught exceptions appropriately (`error instanceof Error`) before accessing properties
- Handle error causes safely: When unwrapping error causes, verify the error is an Error instance first

Example of problematic patterns:
```typescript
// Bad: throwing string
throw `External error with reported id was not registered`

// Bad: inconsistent with function signature that returns undefined
lookupError(error: number): ErrorRecord | undefined {
  if (!errorRecord) throw `External error with reported id was not registered`
  return errorRecord
}

// Bad: unsafe destructuring from any
catch (e) {
  const { message } = e // e is any, not type-safe
}
```

Example of improved patterns:
```typescript
// Good: proper Error object
throw new Error('External error with reported id was not registered')

// Good: consistent with signature
lookupError(error: number): ErrorRecord | undefined {
  const errorRecord = this.registeredErrors[error]
  return errorRecord // returns undefined if not found
}

// Good: type-safe error handling
catch (error) {
  if (error instanceof Error) {
    return err(error.cause)
  }
  throw error
}
```