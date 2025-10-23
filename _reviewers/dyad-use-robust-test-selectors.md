---
title: use robust test selectors
description: E2E tests should use stable, reliable selectors and waiting strategies
  to prevent flaky test failures. Prefer test IDs over CSS class names for element
  selection, as class names may change during refactoring and break tests. Use condition-based
  waits instead of arbitrary timeouts to ensure tests wait for the actual state changes
  rather than fixed time...
repository: dyad-sh/dyad
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 16903
---

E2E tests should use stable, reliable selectors and waiting strategies to prevent flaky test failures. Prefer test IDs over CSS class names for element selection, as class names may change during refactoring and break tests. Use condition-based waits instead of arbitrary timeouts to ensure tests wait for the actual state changes rather than fixed time periods.

Example of robust selector usage:
```typescript
// Avoid: brittle CSS class selector
const chatListItems = await po.page.locator(".chat-list-item");

// Prefer: stable test ID selector  
const chatListItems = await po.page.getByTestId("chat-list-item");

// Avoid: arbitrary timeout
await po.page.waitForTimeout(500);

// Prefer: condition-based wait
await po.page.waitForSelector('[data-testid="search-results"]');
```

This approach makes tests more maintainable and reduces false failures caused by timing issues or UI refactoring.