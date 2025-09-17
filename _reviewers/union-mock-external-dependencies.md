---
title: Mock external dependencies
description: Always mock external dependencies in tests to ensure isolation and reliability.
  Unit tests should not make real network calls, database queries, or interact with
  external services. Mock implementations must provide the same interface and requirements
  as their live counterparts to maintain test validity.
repository: unionlabs/union
label: Testing
language: TypeScript
comments_count: 2
repository_stars: 74800
---

Always mock external dependencies in tests to ensure isolation and reliability. Unit tests should not make real network calls, database queries, or interact with external services. Mock implementations must provide the same interface and requirements as their live counterparts to maintain test validity.

When creating mocks, ensure they:
- Return predictable, controlled responses
- Maintain the same interface as the real implementation
- Provide the same requirements/dependencies as the live version

Example:
```typescript
// Mock GraphQL queries to avoid network calls
vi.mock('../../src/graphql/unwrapped-quote-token.js', async (importOriginal) => {
  return {
    ...await importOriginal<typeof import('../../src/graphql/unwrapped-quote-token.js')>(),
    graphqlQuoteTokenUnwrapQuery: () => Effect.succeed("0x12345")
  }
})

// Mock layers for integration testing
const mockLayer = Layer.empty // must provision same requirements as live layer
```

This approach prevents flaky tests, improves test execution speed, and ensures tests focus on the code under test rather than external system behavior.