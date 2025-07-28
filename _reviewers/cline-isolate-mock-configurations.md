---
title: isolate mock configurations
description: When using Vitest mocking, avoid multiple `vi.mock` calls for the same
  module within a single test file, as mock calls are hoisted and can interfere with
  each other. Instead, organize tests requiring different mock configurations into
  separate test files or test suites with proper setup/teardown.
repository: cline/cline
label: Testing
language: TSX
comments_count: 2
repository_stars: 48299
---

When using Vitest mocking, avoid multiple `vi.mock` calls for the same module within a single test file, as mock calls are hoisted and can interfere with each other. Instead, organize tests requiring different mock configurations into separate test files or test suites with proper setup/teardown.

The issue arises because `vi.mock` calls are hoisted to the top of the file, making it impossible to have different mock implementations for different test scenarios in the same file. This can cause tests to break unexpectedly when mock configurations conflict.

**Problematic approach:**
```typescript
// This won't work as expected - both mocks target the same module
vi.mock("../../../context/ExtensionStateContext", () => ({
  useExtensionState: vi.fn(() => ({ apiProvider: "openai" }))
}))

vi.mock("../../../context/ExtensionStateContext", () => ({
  useExtensionState: vi.fn(() => ({ apiProvider: "nebius" }))
}))
```

**Better approach:**
- Create separate test files for different API providers
- Use `beforeEach`/`afterEach` to modify mock return values within the same mock setup
- Group related test scenarios that share the same mock configuration

This ensures test isolation and prevents one test's mock configuration from breaking others.