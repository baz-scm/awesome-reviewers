---
title: Strategic telemetry implementation
description: Implement telemetry collection strategically to ensure system reliability
  and meaningful data capture. Place telemetry calls where relevant context is available,
  use non-blocking patterns for time-sensitive operations, and avoid unnecessary abstraction.
repository: cline/cline
label: Observability
language: TypeScript
comments_count: 4
repository_stars: 48299
---

Implement telemetry collection strategically to ensure system reliability and meaningful data capture. Place telemetry calls where relevant context is available, use non-blocking patterns for time-sensitive operations, and avoid unnecessary abstraction.

Key principles:
1. **Non-blocking in critical paths**: Use fire-and-forget patterns or periodic collection for operations with strict time limits
2. **Context-aware placement**: Capture metrics where you have access to the relevant data and user actions
3. **Avoid over-engineering**: Don't create unnecessary abstractions for single-use telemetry calls
4. **Be intentional**: Focus on metrics that provide actionable insights about feature usage and error rates

Example implementation:
```typescript
// Good: Periodic collection with non-blocking pattern
const thirtyMinutes = 30 * 60 * 1000
telemetryIntervalId = setInterval(() => {
    // Fire-and-forget, log potential errors but don't block
    void telemetryService.sendCollectedEvents().catch((error) => {
        Logger.error("Error sending periodic telemetry:", error)
    })
}, thirtyMinutes)

// Good: Capture at the point where context is available
const options = parsePartialArrayString(optionsRaw || "[]")
this.lastOptionsCount = options.length

// Good: Direct usage instead of unnecessary abstraction
telemetryService.captureTaskRestarted(this.taskId, apiConfiguration.apiProvider)
```