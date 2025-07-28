---
title: Set evidence-based timeouts
description: Configure timeout values based on empirical testing and user experience
  requirements rather than arbitrary durations. Analyze actual system behavior to
  determine appropriate timeout thresholds that balance responsiveness with reliability.
repository: cline/cline
label: Performance Optimization
language: TypeScript
comments_count: 3
repository_stars: 48299
---

Configure timeout values based on empirical testing and user experience requirements rather than arbitrary durations. Analyze actual system behavior to determine appropriate timeout thresholds that balance responsiveness with reliability.

For user-facing operations, implement progressive feedback mechanisms - start with shorter timeouts for warnings while allowing longer timeouts for actual failures. For example, warn users after 7 seconds but don't abandon the operation until 15 seconds.

For system operations, test with realistic scenarios to determine optimal values. Shell integration consistently emits initial chunks within milliseconds, so a 500ms timeout is sufficient for detecting unresponsive processes.

```typescript
// Good: Evidence-based timeout with progressive feedback
let checkpointsWarningTimer: NodeJS.Timeout | null = null
checkpointsWarningTimer = setTimeout(async () => {
    if (!checkpointsWarningShown) {
        checkpointsWarningShown = true
        this.taskState.checkpointTrackerErrorMessage = 
            "Checkpoints are taking longer than expected to initialize..."
        await this.postStateToWebview()
    }
}, 7_000) // Warn at 7s, but don't abandon until 15s

// Good: Tested timeout for system operations  
const timeoutMs = 500 // Verified: shell integration emits chunks within milliseconds
firstChunkTimeout = setTimeout(() => {
    // Handle timeout case
}, timeoutMs)
```

Always include timeout handling to prevent indefinite blocking and maintain application responsiveness, especially for network operations and external process interactions.