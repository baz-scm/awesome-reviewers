---
title: Ensure comprehensive test coverage
description: Always verify that tests cover all relevant scenarios, edge cases, and
  conditions rather than just the happy path. When reviewing or writing tests, actively
  look for missing test cases and suggest additional coverage.
repository: electron/electron
label: Testing
language: TypeScript
comments_count: 6
repository_stars: 117644
---

Always verify that tests cover all relevant scenarios, edge cases, and conditions rather than just the happy path. When reviewing or writing tests, actively look for missing test cases and suggest additional coverage.

Key areas to examine:
- **Edge cases and boundary conditions**: Test both positive and negative values, empty/null inputs, and limit cases
- **Platform-specific behavior**: Ensure tests cover different operating systems when functionality varies
- **Error conditions**: Test failure scenarios, non-zero exit codes, and exception handling  
- **Security-critical features**: Comprehensive testing is essential for security features before stable release
- **Different input types**: Test various URL types, data formats, and configuration options

Example from the discussions:
```typescript
// Instead of just testing the basic case
it('window opened with innerWidth option has the same innerWidth', async () => {
  // ... basic test
});

// Also test against related functionality
it('should also test against win.getContentSize()', async () => {
  // ... additional coverage
});

// And test edge cases
it('emits the resize event for single-pixel size changes', async () => {
  const [width, height] = w.getSize();
  const size = [width + 1, height - 1]; // Test both + and - changes
});
```

When you encounter a test that seems to work "incidentally" or only covers one scenario, ask: "What other conditions should this handle?" and "Are we missing any important edge cases?"