---
title: preserve error context
description: When propagating errors through promise rejections, catch blocks, or
  error transformations, always preserve the original error information to maintain
  debugging context and error traceability.
repository: rocicorp/mono
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 2091
---

When propagating errors through promise rejections, catch blocks, or error transformations, always preserve the original error information to maintain debugging context and error traceability.

Common anti-patterns include:
- Rejecting promises without the original error: `reject()` instead of `reject(error)`
- Generic error messages that lose specifics: `"An error occurred"` instead of the actual error
- Not handling unknown error types properly when extracting messages

**Good practices:**

```typescript
// ✅ Pass the original error when rejecting
} catch (error) {
  this.#setTransactionEnded(true, error);
  reject(error); // Preserve the original error
}

// ✅ Handle unknown error types safely while preserving info
function makeAppErrorResponse(m: Mutation, e: unknown): MutationResponse {
  return {
    result: {
      error: 'app',
      details: e instanceof Error ? e.message : String(e), // Convert unknown to string
    }
  };
}

// ✅ Return rejected promises instead of sync throws in async contexts
run(): Promise<HumanReadable<TReturn>> {
  return Promise.reject(new Error('AuthQuery cannot be run'));
}
```

This practice significantly improves debugging experience by maintaining the full error chain and context, making it easier to trace issues back to their root cause.