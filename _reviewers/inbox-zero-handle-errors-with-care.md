---
title: Handle errors with care
description: Always implement comprehensive error handling for asynchronous operations,
  external API calls, and database operations. Catch errors at appropriate levels,
  log them with sufficient context for debugging, and provide meaningful error responses
  or recovery mechanisms.
repository: elie222/inbox-zero
label: Error Handling
language: TypeScript
comments_count: 10
repository_stars: 8267
---

Always implement comprehensive error handling for asynchronous operations, external API calls, and database operations. Catch errors at appropriate levels, log them with sufficient context for debugging, and provide meaningful error responses or recovery mechanisms.

Key principles:
1. Use try/catch blocks for error-prone operations
2. Log errors with relevant context
3. Implement recovery or fallback mechanisms
4. Return consistent error responses

Example:
```typescript
async function processUserData(userId: string) {
  try {
    // Attempt primary operation
    const result = await database.users.findUnique({
      where: { id: userId },
    });
    
    if (!result) {
      logger.warn("User not found", { userId });
      return { error: "User not found" };
    }
    
    try {
      // Attempt secondary operation
      await externalApi.process(result);
      return { success: true };
    } catch (error) {
      // Handle specific operation failure
      logger.error("API processing failed", {
        userId,
        error: error instanceof Error ? error.message : String(error),
      });
      // Attempt fallback or recovery
      return { error: "Processing failed", retry: true };
    }
  } catch (error) {
    // Handle critical failures
    logger.error("Critical database error", {
      userId,
      error: error instanceof Error ? error.stack : String(error),
    });
    throw new Error("Internal server error");
  }
}
```

This approach ensures:
- Errors are caught and handled appropriately
- Error context is preserved for debugging
- Users receive meaningful error messages
- System can attempt recovery when possible