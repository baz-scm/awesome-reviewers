---
title: Configuration override precedence
description: When designing systems with configurations that can be specified at multiple
  levels (global vs local, environment vs file, default vs override), establish and
  document a clear precedence model. Always prioritize more specific configurations
  over general ones.
repository: hashicorp/terraform
label: Configurations
language: Go
comments_count: 4
repository_stars: 45532
---

When designing systems with configurations that can be specified at multiple levels (global vs local, environment vs file, default vs override), establish and document a clear precedence model. Always prioritize more specific configurations over general ones.

For example, with test configurations:
```go
// Apply local run block settings over global test block settings
if runBlock.SkipCleanup != nil {
    // Local setting takes precedence when explicitly set
    useSkipCleanup = *runBlock.SkipCleanup
} else if testBlock.SkipCleanup != nil {
    // Fall back to global setting when local isn't specified
    useSkipCleanup = *testBlock.SkipCleanup
}
```

Use pointers for optional configuration values to distinguish between unset values (nil) and explicit zero values. This pattern enables clear differentiation between "not specified" and "explicitly set to default value", allowing proper inheritance from parent configurations.

When designing hierarchical configurations, document the precedence rules to help users understand which settings will take effect when specified at multiple levels. This is especially important for complex systems like backends, providers, and test frameworks.