---
title: Add unit tests
description: All new functionality must include corresponding unit tests. This is
  especially critical for utility functions, core logic modules, stream processing,
  data transformation methods, and complex business logic. Without unit tests, code
  becomes difficult to understand and maintain over time.
repository: lobehub/lobe-chat
label: Testing
language: TypeScript
comments_count: 7
repository_stars: 65138
---

All new functionality must include corresponding unit tests. This is especially critical for utility functions, core logic modules, stream processing, data transformation methods, and complex business logic. Without unit tests, code becomes difficult to understand and maintain over time.

Key areas that require unit tests:
- Utility functions and helper methods that can be extracted and tested independently
- Core logic modules that handle critical business functionality
- Stream processing and asynchronous operations
- Data transformation and parsing methods
- Error handling and edge cases
- New features with conditional logic

Example test structure for a utility function:
```typescript
// For a model parsing utility
describe('detectModelProvider', () => {
  it('should detect anthropic provider for claude models', () => {
    expect(detectModelProvider('claude-3-sonnet')).toBe('anthropic');
  });
  
  it('should default to openai for unknown models', () => {
    expect(detectModelProvider('unknown-model')).toBe('openai');
  });
});
```

When adding tests, ensure proper mocking of external dependencies and use appropriate test setup (providers, wrappers) to avoid test environment issues. Tests should cover both happy path scenarios and error cases to maintain code reliability.