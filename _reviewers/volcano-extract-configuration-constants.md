---
title: Extract configuration constants
description: Avoid hardcoded values and magic numbers in configuration-related code
  by extracting them as named constants. This improves code maintainability, readability,
  and makes configuration values easier to modify.
repository: volcano-sh/volcano
label: Configurations
language: Go
comments_count: 3
repository_stars: 4899
---

Avoid hardcoded values and magic numbers in configuration-related code by extracting them as named constants. This improves code maintainability, readability, and makes configuration values easier to modify.

Hardcoded values make code difficult to understand and maintain. When configuration values, timeouts, or default settings are embedded directly in the code, it becomes unclear what these values represent and makes them harder to change consistently across the codebase.

**Examples of what to extract:**

```go
// Bad: Magic numbers and hardcoded strings
if resourceStrategyFitPluginWeight <= 0 {
    resourceStrategyFitPluginWeight = 10  // What does 10 represent?
}

data, ok := cm.Data["device-config.yaml"]  // Hardcoded key

if !exist || nowTs-ts > 60 {  // What does 60 seconds represent?
```

**Good: Extract as named constants:**

```go
const (
    DefaultResourceStrategyFitWeight = 10
    DeviceConfigKey = "device-config.yaml"
    TaskStatusUpdateIntervalSeconds = 60
)

// Usage
if resourceStrategyFitPluginWeight <= 0 {
    resourceStrategyFitPluginWeight = DefaultResourceStrategyFitWeight
}

data, ok := cm.Data[DeviceConfigKey]

if !exist || nowTs-ts > TaskStatusUpdateIntervalSeconds {
```

**Apply this practice to:**
- Default configuration values and weights
- Timeout intervals and retry counts  
- Configuration file keys and field names
- Feature flag names and environment variable keys
- Any numeric or string literals that represent configurable behavior

This makes the code self-documenting and centralizes configuration values for easier maintenance.