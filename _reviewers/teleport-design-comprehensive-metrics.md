---
title: Design comprehensive metrics
description: When designing observability metrics, ensure they are explicit about
  all possible states, comprehensive in scope, and clearly documented to avoid ambiguity.
  Metrics should accurately represent what is being monitored and make their limitations
  transparent.
repository: gravitational/teleport
label: Observability
language: Markdown
comments_count: 2
repository_stars: 19109
---

When designing observability metrics, ensure they are explicit about all possible states, comprehensive in scope, and clearly documented to avoid ambiguity. Metrics should accurately represent what is being monitored and make their limitations transparent.

Key principles:
1. **Explicit state representation**: Use separate metrics for each distinct state rather than requiring calculations. For example, use `teleport_resources_health_status_healthy`, `teleport_resources_health_status_unhealthy`, and `teleport_resources_health_status_unknown` instead of forcing users to calculate unknown states.

2. **Clear scope documentation**: Explicitly document what resources are included in metrics. If metrics only count resources with health checks enabled, this limitation must be clearly stated to prevent false assumptions about system coverage.

3. **Comprehensive coverage**: When implementing health checks for a resource type, always include all instances in the monitoring system, even if they're disabled. Mark disabled instances with appropriate status (e.g., `status: unknown, reason: disabled`) rather than excluding them entirely.

Example implementation:
```go
// Good: Explicit metrics for each state
resourcesHealthyGauge = prometheus.NewGaugeVec(
    prometheus.GaugeOpts{
        Name: "teleport_resources_health_status_healthy",
        Help: "Number of resources in healthy state with health checks enabled",
    },
    []string{"type"}, // db|kubernetes|etc
)

resourcesUnhealthyGauge = prometheus.NewGaugeVec(
    prometheus.GaugeOpts{
        Name: "teleport_resources_health_status_unhealthy", 
        Help: "Number of resources in unhealthy state with health checks enabled",
    },
    []string{"type"},
)
```

This approach prevents confusion about metric scope, enables accurate alerting, and provides clear visibility into system state without requiring complex calculations.