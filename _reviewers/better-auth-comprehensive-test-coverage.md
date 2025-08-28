---
title: comprehensive test coverage
description: When adding new functionality, configuration options, or plugins, always
  include corresponding tests that verify the feature works as expected. Tests should
  comprehensively cover all aspects of the functionality, including input/output validation,
  data transformations, and edge cases. Additionally, structure tests as focused,
  single-responsibility test...
repository: better-auth/better-auth
label: Testing
language: TypeScript
comments_count: 3
repository_stars: 19651
---

When adding new functionality, configuration options, or plugins, always include corresponding tests that verify the feature works as expected. Tests should comprehensively cover all aspects of the functionality, including input/output validation, data transformations, and edge cases. Additionally, structure tests as focused, single-responsibility test cases rather than combining multiple concerns into one test.

For example, when adding a bearer token plugin to a client configuration:
```ts
// Bad: Adding plugin without tests
const client = createAuthClient({
  plugins: [bearerClient()], // No tests verify this works
});

// Good: Adding plugin with comprehensive tests
describe('Bearer Token Plugin', () => {
  test('should authenticate with bearer token', async () => {
    // Test the plugin functionality
  });
  
  test('should handle invalid bearer tokens', async () => {
    // Test error cases
  });
});
```

When testing data transformations, verify both the transformation process and the final output. For array-to-string conversions, test that `["medium", "large"]` transforms to `'["medium","large"]'` during storage and back to the original array when retrieved.