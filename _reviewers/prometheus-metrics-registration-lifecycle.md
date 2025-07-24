---
title: metrics registration lifecycle
description: Ensure proper metrics registration and lifecycle management to maintain
  observability system stability. Handle metric registration/unregistration correctly
  during configuration changes and avoid common pitfalls that can cause panics or
  data loss.
repository: prometheus/prometheus
label: Observability
language: Go
comments_count: 8
repository_stars: 59616
---

Ensure proper metrics registration and lifecycle management to maintain observability system stability. Handle metric registration/unregistration correctly during configuration changes and avoid common pitfalls that can cause panics or data loss.

Key practices:
1. **Use AlreadyRegisteredError pattern for shared metrics**: When multiple components share the same metrics, handle registration conflicts gracefully by retrieving existing metrics from the registry instead of creating new ones.

2. **Manage registration during config reloads**: Properly unregister metrics before re-registering to avoid panics, but be aware this causes counter resets. Consider keeping metrics registered and reusing them when possible.

3. **Register all required collectors**: When using custom registries, ensure all necessary collectors (GoCollector, ProcessCollector) are registered, not just the default ones.

Example of proper AlreadyRegisteredError handling:
```go
func newDiscovererMetrics(reg prometheus.Registerer) *zookeeperMetrics {
    m := &zookeeperMetrics{
        failureCounter: prometheus.NewCounter(prometheus.CounterOpts{
            Name: "zookeeper_failures_total",
            Help: "The total number of ZooKeeper failures.",
        }),
    }
    
    // Handle shared metrics between components
    if err := reg.Register(m.failureCounter); err != nil {
        if are, ok := err.(prometheus.AlreadyRegisteredError); ok {
            // Use the existing metric instead of the new one
            m.failureCounter = are.ExistingCollector.(prometheus.Counter)
        } else {
            // Handle other registration errors
            return nil
        }
    }
    return m
}
```

This prevents registration panics while ensuring metrics remain functional across component lifecycles and configuration changes.