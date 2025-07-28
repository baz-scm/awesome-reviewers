---
title: Feature flag isolation
description: Feature flags should be properly isolated and scoped to avoid mixing
  configuration concerns with core interfaces. When implementing feature flags, ensure
  they only affect behavior when explicitly enabled and don't leak into unrelated
  system components.
repository: facebook/react-native
label: Configurations
language: Kotlin
comments_count: 3
repository_stars: 123178
---

Feature flags should be properly isolated and scoped to avoid mixing configuration concerns with core interfaces. When implementing feature flags, ensure they only affect behavior when explicitly enabled and don't leak into unrelated system components.

Key principles:
- Keep feature flags out of core interfaces that will outlive the flag
- Ensure behavior changes are isolated to when flags are enabled 
- Document flag limitations and dependencies clearly
- Avoid mixing UI configuration with system-level interfaces

Example of proper isolation:
```kotlin
// Instead of adding to core interface
public interface ReactHost {
  public fun isEdgeToEdgeEnabled(): Boolean // ❌ Avoid
}

// Use scoped utility or check flag directly where needed
if (isEdgeToEdgeFeatureFlagOn) {
  // Feature-specific behavior only when flag is on
  windowDisplayMetrics.setTo(displayMetrics)
}
```

Always document flag constraints:
```properties
# Enables edge-to-edge. Only works with ReactActivity and should not be used with custom Activity.
edgeToEdgeEnabled=false
```

This prevents configuration complexity from spreading throughout the codebase and makes it easier to remove flags when features become default.