---
title: Health check lifecycle completeness
description: 'Ensure health check systems are not only created but also properly launched
  and integrated with observability infrastructure. Health checkers must follow the
  complete lifecycle: creation, launch, and metrics integration.'
repository: traefik/traefik
label: Observability
language: Go
comments_count: 2
repository_stars: 55772
---

Ensure health check systems are not only created but also properly launched and integrated with observability infrastructure. Health checkers must follow the complete lifecycle: creation, launch, and metrics integration.

When implementing health checks, verify that:
1. Health checkers are created during service setup
2. Health checkers are explicitly launched (not just instantiated)
3. Metrics collection is properly integrated
4. The implementation follows established patterns from similar components

Example of incomplete implementation:
```go
// TCP health checkers created but never launched
if conf.LoadBalancer.HealthCheck != nil {
    m.healthCheckers[serviceName] = healthcheck.NewServiceTCPHealthChecker(
        ctx,
        m.dialerManager,
        nil, // metrics parameter passed as nil
        // ... other params
    )
    // Missing: no launch call equivalent to serviceManager.LaunchHealthCheck(ctx)
}
```

Compare this with HTTP health checkers that properly launch via `serviceManager.LaunchHealthCheck(ctx)` and integrate metrics. TCP health checks should follow the same complete lifecycle pattern to ensure proper observability and functionality.