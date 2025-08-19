---
title: Verify error handling paths
description: When implementing error handling logic, ensure that both the behavior
  and reasoning are clear, and that error paths are properly tested at appropriate
  levels. For methods that handle missing data, the default behavior should be explicitly
  documented and the method name should clearly indicate what the return value represents.
  For exception handling, verify...
repository: PostHog/posthog
label: Error Handling
language: TypeScript
comments_count: 2
repository_stars: 28460
---

When implementing error handling logic, ensure that both the behavior and reasoning are clear, and that error paths are properly tested at appropriate levels. For methods that handle missing data, the default behavior should be explicitly documented and the method name should clearly indicate what the return value represents. For exception handling, verify that upstream code properly catches and handles the exceptions to ensure graceful failure.

Example from the discussions:
```typescript
// Good: Clear method name and documented default behavior
private async isRecipientOptedOutOfAction(invocation, action): Promise<boolean> {
    // ... logic to find recipient
    if (!recipient) {
        // Default to opted-in if no preference exists (per TOS)
        return false; // false = not opted out = can send message
    }
    // ... rest of logic
}

// When throwing exceptions, ensure upstream handling exists
if (this.isPropertiesSizeConstraintViolation(error)) {
    logger.warn('Rejecting person properties create/update, exceeds size limit', {
        team_id: teamId,
        violation_type: 'create_person_size_violation',
    });
    throw new PersonPropertiesSizeViolationError(/* ... */);
}
```

Always verify that exception handling is tested at the service level to ensure the application fails gracefully rather than crashing unexpectedly.