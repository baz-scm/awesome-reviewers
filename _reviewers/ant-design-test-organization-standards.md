---
title: Test organization standards
description: Write tests that are well-organized, maintainable, and reflect real usage
  patterns. Test names should describe behavior and requirements rather than implementation
  details. Group related tests under appropriate describe blocks and avoid redundant
  test cases.
repository: ant-design/ant-design
label: Testing
language: TSX
comments_count: 4
repository_stars: 95882
---

Write tests that are well-organized, maintainable, and reflect real usage patterns. Test names should describe behavior and requirements rather than implementation details. Group related tests under appropriate describe blocks and avoid redundant test cases.

Key principles:
- Name tests based on expected behavior: "should prevent multiple clicks when loading" instead of "should update loading state correctly when using ref"
- Group related tests logically: Use one describe block per feature/component area rather than creating separate describes for single test cases
- Test through realistic component usage patterns rather than isolated utility functions to ensure proper coverage
- Remove or consolidate redundant tests when new test cases already cover the same scenarios
- Extract complex test scenarios into dedicated test files (e.g., semantic.test.tsx) for better organization

Example of good test organization:
```typescript
describe('CheckableTag', () => {
  it('should render icon when provided', () => {
    // Test icon rendering behavior
  });
  
  it('should handle click events correctly', () => {
    // Test click behavior
  });
  
  it('should support custom classNames and styles', () => {
    // Test styling behavior
  });
});
```

This approach makes tests easier to navigate, maintain, and ensures they accurately reflect how components are actually used in applications.