---
title: Prevent flaky test timing
description: 'Replace non-deterministic timing patterns with reliable alternatives
  to prevent flaky tests. This includes:


  1. Use element-based waits instead of fixed timeouts:'
repository: langfuse/langfuse
label: Testing
language: TypeScript
comments_count: 4
repository_stars: 13574
---

Replace non-deterministic timing patterns with reliable alternatives to prevent flaky tests. This includes:

1. Use element-based waits instead of fixed timeouts:
```typescript
// Bad
await page.waitForTimeout(2000);

// Good
await page.waitForSelector('[data-testid="element"]', { 
  state: 'visible',
  timeout: 5000 
});
```

2. Use fixed timestamps for time-dependent tests:
```typescript
// Bad
const cutoffDate = new Date(Date.now() + 24*60*60*1000);

// Good
const cutoffDate = new Date('2024-01-01T00:00:00Z');
```

3. Mock time-based functions when testing time-dependent logic:
```typescript
// Bad
const job = await createJob({ 
  timestamp: new Date() 
});

// Good
const fixedDate = new Date('2024-01-01T00:00:00Z');
jest.useFakeTimers().setSystemTime(fixedDate);
const job = await createJob({ 
  timestamp: new Date() 
});
```

This approach reduces test flakiness, improves CI reliability, and makes tests more maintainable by removing timing-dependent assumptions.