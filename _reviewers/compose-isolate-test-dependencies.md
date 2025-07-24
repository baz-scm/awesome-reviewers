---
title: Isolate test dependencies
description: Keep test dependencies separate from production code dependencies to
  avoid polluting the main module. Use separate modules for test code when test-specific
  dependencies would otherwise be included in the main module's dependency tree.
repository: docker/compose
label: Testing
language: Other
comments_count: 2
repository_stars: 35858
---

Keep test dependencies separate from production code dependencies to avoid polluting the main module. Use separate modules for test code when test-specific dependencies would otherwise be included in the main module's dependency tree.

This prevents test libraries from becoming transitive dependencies for consumers of your module and maintains a cleaner separation between production and test concerns.

Example approach:
```go
// Create separate go.mod for e2e tests
// e2e/go.mod
module github.com/docker/compose/v2/e2e

require (
    github.com/cucumber/godog v0.12.5
    github.com/docker/compose/v2 v0.0.0
)

replace github.com/docker/compose/v2 => ../
```

This pattern allows test-specific dependencies like testing frameworks, mocking libraries, or specialized test utilities to remain isolated from the main codebase while still allowing tests to import and test the production code.