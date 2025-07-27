---
title: Graceful error handling
description: Implement robust error handling that provides fallback mechanisms, ensures
  proper resource cleanup, and delivers user-friendly error messages without exposing
  internal details.
repository: snyk/cli
label: Error Handling
language: TypeScript
comments_count: 10
repository_stars: 5178
---

Implement robust error handling that provides fallback mechanisms, ensures proper resource cleanup, and delivers user-friendly error messages without exposing internal details.

Key principles:
1. **Use finally blocks for cleanup**: When modifying global state or resources, always reset them in finally blocks to prevent resource leaks when errors occur
2. **Provide fallback mechanisms**: When primary operations fail (like JSON serialization), implement fallback strategies rather than failing completely
3. **Check error types, not messages**: Use `instanceof Error` or specific error types rather than fragile string matching on error messages
4. **Handle unexpected scenarios gracefully**: When encountering unexpected conditions, log debug information and provide user-friendly error messages
5. **Avoid exposing internal details**: Don't leak internal error messages or stack traces to external users; provide sanitized, actionable error messages

Example implementation:
```typescript
// Good: Proper cleanup and fallback
export async function processWithCleanup(config: Config): Promise<string> {
  let originalValue;
  try {
    originalValue = global.someProperty;
    global.someProperty = newValue;
    
    const result = await riskyOperation();
    
    // Fallback for serialization
    try {
      return JSON.stringify(result, null, 2);
    } catch (serializationError) {
      debug('JSON.stringify failed, trying without pretty print', serializationError);
      return JSON.stringify(result);
    }
  } catch (error) {
    // Type-based error handling
    if (error instanceof CustomError) {
      return handleCustomError(error);
    }
    
    // Graceful handling of unexpected errors
    debug(`Unexpected error: ${error}`);
    throw new UserFriendlyError('Operation failed. Please try again or contact support.');
  } finally {
    // Always cleanup, regardless of success or failure
    if (originalValue !== undefined) {
      global.someProperty = originalValue;
    }
  }
}
```

This approach ensures applications remain stable and user-friendly even when encountering unexpected conditions or failures.