---
title: Add tests for functionality
description: New functionality should include corresponding tests to ensure code quality
  and maintainability. When introducing new methods, utilities, or services, always
  add appropriate test coverage.
repository: twentyhq/twenty
label: Testing
language: TypeScript
comments_count: 5
repository_stars: 35477
---

New functionality should include corresponding tests to ensure code quality and maintainability. When introducing new methods, utilities, or services, always add appropriate test coverage.

For new utility functions or services, consider starting with integration tests as they are often more maintainable and require less mocking. For complex logic that would benefit from isolated testing, extract the functionality into a separate utility that can be easily unit tested.

Example approach:
```typescript
// When adding a new service method like toggleInterval()
async toggleInterval(workspace: Workspace) {
  const billingSubscription = await this.getCurrentBillingSubscriptionOrThrow(
    { workspaceId: workspace.id },
  );

  return billingSubscription.interval === SubscriptionInterval.Year
    ? this.switchToMonthlyInterval(billingSubscription)
    : this.switchToYearlyInterval(billingSubscription);
}

// Add corresponding integration test
describe('BillingSubscriptionService', () => {
  it('should toggle billing interval correctly', async () => {
    // Test implementation using makeGraphqlAPIRequest
  });
});
```

This practice helps catch regressions early, documents expected behavior, and makes the codebase more reliable for future development.