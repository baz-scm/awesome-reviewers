---
title: Dynamic config usage principles
description: 'Use dynamic configuration selectively and effectively by following these
  principles:


  1. Only use dynamic config for values that need runtime modification:'
repository: temporalio/temporal
label: Configurations
language: Go
comments_count: 4
repository_stars: 14953
---

Use dynamic configuration selectively and effectively by following these principles:

1. Only use dynamic config for values that need runtime modification:
```go
// Don't use dynamic config for test-only or static values
RateLimiterRefreshInterval: time.Minute, // Static value

// Use dynamic config for runtime-configurable values
SlowRequestThreshold: dc.GetDurationProperty(
    dynamicconfig.SlowRequestLogThreshold,
    5 * time.Second,
)
```

2. Document config parameters with clear impact descriptions:
```go
// Bad: Unclear impact
MaxRetryAttempts = NewGlobalIntSetting(
    "workflow.maxRetryAttempts",
    5,
    "Maximum retry attempts allowed"
)

// Good: Clear threshold impact
MaxRetryAttempts = NewGlobalIntSetting(
    "workflow.maxRetryAttempts",
    5,
    "Maximum retry attempts allowed. When exceeded, workflow fails permanently"
)
```

3. Inject specific config functions instead of entire config collections:
```go
// Bad: Injecting entire config collection
func NewHandler(dc *dynamicconfig.Collection) {
    threshold := dc.GetDurationProperty(...)
}

// Good: Injecting specific config function
func NewHandler(thresholdFn dynamicconfig.DurationPropertyFn) {
    threshold := thresholdFn()
}
```

This approach improves testability, maintainability, and makes configuration dependencies explicit while ensuring configs are used only where runtime modification is necessary.