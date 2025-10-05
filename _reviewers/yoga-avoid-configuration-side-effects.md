---
title: Avoid configuration side effects
description: Configuration properties should behave predictably without hidden side
  effects that override explicitly set values. When a developer sets a configuration
  value, the system should respect that value rather than applying additional logic
  that might change the effective behavior.
repository: facebook/yoga
label: Configurations
language: Objective-C
comments_count: 2
repository_stars: 18255
---

Configuration properties should behave predictably without hidden side effects that override explicitly set values. When a developer sets a configuration value, the system should respect that value rather than applying additional logic that might change the effective behavior.

Avoid implementing getters that can return different values than what was explicitly set, as this creates confusion and makes the system harder to reason about. If complex logic is needed to determine effective configuration state, consider separating the user-facing configuration from the computed state.

Example of problematic pattern:
```objc
- (BOOL)isEnabled
{
  if (!super.isEnabled) {
    return NO;  // Side effect: can return NO even if explicitly set to YES
  }
  // Additional complex logic here...
}
```

Instead, use clear separation between configuration and computed state:
```objc
- (BOOL)isEnabled
{
  return _isEnabled;  // Returns exactly what was set
}

- (BOOL)isIncludedInLayout
{
  return self.isEnabled && [self meetsOtherCriteria];  // Separate computed property
}
```

This approach makes the configuration behavior transparent and the codebase easier to maintain and debug.