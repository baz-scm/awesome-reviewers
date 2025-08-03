---
title: Never swallow errors silently
description: Always handle errors explicitly and preserve their context. Never silently
  catch and discard errors as this hides bugs and makes debugging difficult. When
  re-throwing errors, include the original error as the cause to maintain the stack
  trace. In UI components, convert errors to user-friendly messages while logging
  technical details at appropriate levels.
repository: n8n-io/n8n
label: Error Handling
language: TypeScript
comments_count: 6
repository_stars: 122978
---

Always handle errors explicitly and preserve their context. Never silently catch and discard errors as this hides bugs and makes debugging difficult. When re-throwing errors, include the original error as the cause to maintain the stack trace. In UI components, convert errors to user-friendly messages while logging technical details at appropriate levels.

Example of proper error handling:

```typescript
// ❌ Bad - Silently swallowing error
try {
  await apiRequest();
} catch {
  // Error silently ignored
}

// ❌ Bad - Losing error context
try {
  await apiRequest(); 
} catch (error) {
  throw new Error('API request failed');
}

// ✅ Good - Preserving context and handling appropriately
try {
  await apiRequest();
} catch (error) {
  // Log technical details
  logger.error('API request failed', error);
  
  // In UI: Show user-friendly message
  toast.showError(
    new Error('Unable to complete request', { cause: error }),
    'Action failed'
  );
  
  // In services: Re-throw with context
  throw new OperationalError(
    'API request failed',
    { cause: error }
  );
}
```