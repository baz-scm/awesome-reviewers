---
title: Conditional observability instrumentation
description: 'Wrap all tracing, profiling, and debugging instrumentation in appropriate
  conditional compilation blocks (like `MLN_TRACY_ENABLE`) to prevent performance
  overhead in production builds. When adding trace points:'
repository: maplibre/maplibre-native
label: Observability
language: C++
comments_count: 2
repository_stars: 1411
---

Wrap all tracing, profiling, and debugging instrumentation in appropriate conditional compilation blocks (like `MLN_TRACY_ENABLE`) to prevent performance overhead in production builds. When adding trace points:

1. Use proper scoping for trace zones to control their lifetime
2. Include contextual information with zone annotations to maximize debugging value
3. Consider the performance impact of unique identifiers and other debug-only information

Example:
```cpp
// Good practice - scoped and conditionally compiled
#ifdef MLN_TRACY_ENABLE
{
    MLN_TRACE_FUNC()
    MLN_ZONE_STR(name)  // Adds context about which component is being processed
}
#endif

// For debug IDs or other observability-only fields
class MyClass {
private:
#ifdef MLN_TRACY_ENABLE
    int64_t uniqueDebugId{generateDebugId()};
#endif
    // other members
};
```

This approach ensures that observability instrumentation provides maximum value during development and debugging while having zero impact on production performance.