---
title: Maintain test state isolation
description: Ensure each test runs in isolation by properly managing test state, mocks,
  and timers. Clean up all test artifacts in beforeEach/afterEach hooks rather than
  within individual tests to prevent state leakage and test interdependence.
repository: n8n-io/n8n
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 122978
---

Ensure each test runs in isolation by properly managing test state, mocks, and timers. Clean up all test artifacts in beforeEach/afterEach hooks rather than within individual tests to prevent state leakage and test interdependence.

Example:
```typescript
describe('MyComponent', () => {
  // ❌ Bad: Global mock without cleanup
  const globalMock = vi.spyOn(global, 'setTimeout');

  // ✅ Good: Proper setup and cleanup
  let timeoutSpy: SpyInstance;
  
  beforeEach(() => {
    timeoutSpy = vi.spyOn(global, 'setTimeout');
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.useRealTimers();
  });

  it('should handle timeouts', () => {
    vi.useFakeTimers();
    // Test implementation
  });
});
```

Key practices:
- Use beforeEach/afterEach hooks for consistent setup/cleanup
- Restore all mocks and spies after each test
- Reset timers and other global state
- Avoid sharing mutable state between tests
- Initialize fresh instances for each test case