---
title: Strategic error handling
description: Implement strategic error handling by properly checking exception types
  and using try/catch blocks to distinguish between user errors and system errors.
  Avoid runtime errors from improper type checking and categorize exceptions based
  on their source and required response.
repository: novuhq/novu
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 37700
---

Implement strategic error handling by properly checking exception types and using try/catch blocks to distinguish between user errors and system errors. Avoid runtime errors from improper type checking and categorize exceptions based on their source and required response.

**Key principles:**
1. **Proper exception type checking**: Verify exception structure before using operators like `in` to avoid runtime errors on primitive values
2. **Strategic try/catch placement**: Use try/catch blocks to separate critical system operations from user input validation
3. **Error categorization**: Distinguish between user input errors (which don't need immediate action) and system errors (which require investigation)

**Example:**
```typescript
// Bad - can cause runtime error on primitive exceptions
const isBadRequestExceptionFromValidationPipe =
  exception instanceof Object &&
  'response' in exception &&  // This fails on primitive values
  'message' in (exception as any).response;

// Good - proper type checking
const isBadRequestExceptionFromValidationPipe =
  exception instanceof Object &&
  typeof exception === 'object' &&
  exception !== null &&
  'response' in exception;

// Strategic try/catch - separate system errors from user errors
try {
  // Critical system operations that indicate internal failures
  scheduledJob = await this.createScheduledUnsnoozeJob(notification, delayAmount);
  snoozedNotification = await this.markNotificationAsSnoozed(command);
  await this.queueJob(scheduledJob, delayAmount);
} catch (error) {
  // Transform to InternalServerErrorException - needs immediate attention
  throw new InternalServerErrorException('System error during snooze operation');
}
// User validation errors outside try/catch bubble up as-is
```

This approach prevents runtime errors from improper exception handling while ensuring system errors are properly categorized and logged for investigation.