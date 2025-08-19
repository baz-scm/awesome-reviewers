---
title: Add monitoring metrics
description: Critical code paths, especially error handling and exception scenarios,
  should include metrics or counters to enable monitoring and alerting. This prevents
  systems from failing silently and provides visibility into system health.
repository: PostHog/posthog
label: Observability
language: TypeScript
comments_count: 2
repository_stars: 28460
---

Critical code paths, especially error handling and exception scenarios, should include metrics or counters to enable monitoring and alerting. This prevents systems from failing silently and provides visibility into system health.

When implementing error handling, background processes, or exception catching, add appropriate metrics that can be used for dashboards and alerts. This is particularly important for services that could degrade gracefully but cause issues over time if problems go unnoticed.

Example:
```typescript
// Before: Silent error handling
(e) => {
    logger.error('Error refreshing team retention periods', e)
}

// After: Add metrics for monitoring
(e) => {
    logger.error('Error refreshing team retention periods', e)
    statsd.increment('retention_service.refresh_error')
}
```

Consider what dashboards and alerts you would want to create when the code is deployed. If you can't easily monitor whether a system is working correctly, add the necessary instrumentation.