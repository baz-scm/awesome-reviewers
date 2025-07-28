---
title: implement resource constraints
description: Implement multiple types of resource constraints with appropriate thresholds
  to prevent performance degradation and resource exhaustion. This includes rate limiting,
  memory thresholds, execution time limits, and queue size bounds.
repository: google-gemini/gemini-cli
label: Performance Optimization
language: TypeScript
comments_count: 5
repository_stars: 65062
---

Implement multiple types of resource constraints with appropriate thresholds to prevent performance degradation and resource exhaustion. This includes rate limiting, memory thresholds, execution time limits, and queue size bounds.

Key constraint types to implement:

**Rate Limiting**: Limit frequency of expensive operations
```typescript
// Only record when RSS is 5%+ above previous high water mark
if (currentRss > previousHighWaterMark * 1.05) {
  recordMemoryUsage(currentRss);
  previousHighWaterMark = currentRss;
}
```

**Time-based Constraints**: Set reasonable timeouts to balance accuracy and user experience
```typescript
// 50ms timeout for protocol detection to avoid blocking users
setTimeout(() => {
  if (!checkFinished) {
    detectionComplete = true;
    resolve(false);
  }
}, 50);
```

**Execution Limits**: Use multiple constraint types for long-running operations
```typescript
interface RunConfig {
  max_time_minutes: number;
  max_turns: number;        // Stop after N iterations
  max_tokens: number;       // Budget for resource consumption
}
```

**Queue Size Bounds**: Prevent unbounded growth with capacity limits
```typescript
// Use FixedDeque with hard capacity limit
const events = new FixedDeque(1000);
const eventsToRetry = eventsToSend.slice(-this.max_retry_events); // Limit retry count
```

These constraints should be configurable and set based on the criticality of the operation - more lenient for user-facing features, stricter for background processes. Always consider the trade-off between resource protection and functionality degradation.