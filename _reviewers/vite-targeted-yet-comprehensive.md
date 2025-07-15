---
title: Targeted yet comprehensive
description: Write focused tests that verify specific functionality without unnecessary
  setup, while still ensuring complete coverage of edge cases. Instead of duplicating
  complex structures, create minimal test cases that target individual features directly.
repository: vitejs/vite
label: Testing
language: JavaScript
comments_count: 2
repository_stars: 74031
---

Write focused tests that verify specific functionality without unnecessary setup, while still ensuring complete coverage of edge cases. Instead of duplicating complex structures, create minimal test cases that target individual features directly.

Example:
```js
// Instead of copying an entire playground setup
// packages/vite/src/node/__tests__/build.spec.ts
describe('JSON stringify', () => {
  test('tree shaking works correctly', async () => {
    // Minimal test configuration
    const config = { json: { stringify: true } }
    // Test-specific assertions
    const result = await buildWith(config)
    expect(result.hasTreeShaking).toBe(true)
  })
  
  // Include tests for all relevant edge cases
  test('handles file:// protocol', async () => {
    // Add specific test for this protocol
  })
})
```

This approach improves maintainability by keeping tests focused while still ensuring adequate coverage. When adding tests, consider what specific functionality needs verification and create the minimal test setup required, but be thorough in covering variations and edge cases.