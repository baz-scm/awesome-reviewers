---
title: Preserve error handling context
description: Always preserve error context by using specific error types, safe error
  handling patterns, and meaningful error messages. This helps with debugging and
  maintains a clear error handling chain.
repository: langfuse/langfuse
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 13574
---

Always preserve error context by using specific error types, safe error handling patterns, and meaningful error messages. This helps with debugging and maintains a clear error handling chain.

Key practices:
1. Use specific error types that match the failure scenario
2. Include relevant context in error messages
3. Safely handle and transform errors
4. Maintain error context when rethrowing

Example:
```typescript
// ❌ Poor error handling
try {
  const data = JSON.parse(response);
} catch (e) {
  throw new Error("Failed to parse");
}

// ✅ Good error handling
try {
  const data = JSON.parse(response);
} catch (e) {
  throw new ValidationError(
    `Failed to parse response: ${e instanceof Error ? e.message : String(e)}. 
     Response: ${response.substring(0, 100)}...`
  );
}

// ✅ Good error handling with context
async function processItem(itemId: string) {
  try {
    const result = await backOff(
      async () => await processWithRetries(itemId)
    );
    return result;
  } catch (e) {
    logger.error(
      `Failed to process item ${itemId}: ${e instanceof Error ? e.message : String(e)}`
    );
    throw new ProcessingError(`Item processing failed: ${itemId}`, { cause: e });
  }
}
```