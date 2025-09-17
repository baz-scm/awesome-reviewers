---
title: use meaningful error types
description: Replace generic exceptions with context-specific error types that provide
  meaningful information about what went wrong. When wrapping errors from external
  libraries, always use the correct error types from those libraries and extract error
  details to preserve debugging information.
repository: unionlabs/union
label: Error Handling
language: TypeScript
comments_count: 3
repository_stars: 74800
---

Replace generic exceptions with context-specific error types that provide meaningful information about what went wrong. When wrapping errors from external libraries, always use the correct error types from those libraries and extract error details to preserve debugging information.

Avoid generic error classes like `NoSuchElementException` or `Error` with string messages. Instead, create domain-specific error types that capture the context and cause of the failure.

When integrating with external libraries, use their specific error types rather than importing error types from unrelated libraries. Always call `extractErrorDetails()` when wrapping external errors to preserve stack traces and debugging information.

Example of what to avoid:
```typescript
// Generic, uninformative error
transferDetails.error = Option.some({ _tag: "NotFound", message: "Transfer not found" })

// Wrong error type from different library
catch: err => new FetchAptosTokenBalanceError({ cause: err as ReadContractErrorType })

// Generic error with string interpolation
catch: e => new Error(`Failed to fetch blockNumber for ${rpc}: ${String(e)}`)
```

Example of proper error handling:
```typescript
// Context-specific error type
transferDetails.error = Option.some(new NoSuchElementException())

// Correct error type with detail extraction
catch: err => new FetchAptosTokenBalanceError({ cause: extractErrorDetails(err) })

// Dedicated function returning TaggedError with extracted details
catch: (error) => new SupabaseError({
  operation: "requestRole", 
  cause: extractErrorDetails(error as Error)
})
```

This approach makes errors more informative for debugging and provides better context for error handling and recovery strategies.