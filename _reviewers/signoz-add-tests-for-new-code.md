---
title: Add tests for new code
description: All new code additions, regardless of complexity, should include corresponding
  unit tests to ensure functionality works as expected and to prevent regressions.
  This applies to new modules, utility functions, and any other code components.
repository: SigNoz/signoz
label: Testing
language: Go
comments_count: 2
repository_stars: 23369
---

All new code additions, regardless of complexity, should include corresponding unit tests to ensure functionality works as expected and to prevent regressions. This applies to new modules, utility functions, and any other code components.

When adding new functionality:
- Create test files for new modules to verify core behavior
- Add basic happy path tests for utility functions covering common input scenarios
- Test edge cases and different input types where applicable

Example from discussions:
```go
// For a new module like spanpercentile/translator.go
func TestBuildSpanPercentileQuery(t *testing.T) {
    // Test the queries getting built
}

// For utility functions like ToNanoSecs
func TestToNanoSecs(t *testing.T) {
    // Test seconds, milliseconds, microseconds, and ns to ns conversions
}
```

Even if the new code might be indirectly tested by consumers, dedicated unit tests provide better isolation, clearer failure diagnostics, and serve as documentation of expected behavior.