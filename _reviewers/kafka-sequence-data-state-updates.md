---
title: sequence data state updates
description: When working with distributed data systems, ensure that state updates
  are performed in the correct conceptual order to maintain data consistency and avoid
  race conditions. Operations that logically depend on each other should be sequenced
  appropriately, and components should maintain clear ownership of their data state.
repository: apache/kafka
label: Database
language: Other
comments_count: 3
repository_stars: 30575
---

When working with distributed data systems, ensure that state updates are performed in the correct conceptual order to maintain data consistency and avoid race conditions. Operations that logically depend on each other should be sequenced appropriately, and components should maintain clear ownership of their data state.

For example, when updating watermarks and offsets, perform the logical data update first, then update the watermark:

```scala
// Update the last written offset first
updateLastWrittenOffset(newOffset)

// Then update the high watermark
val currentHighWatermark = log.highWatermark
if (currentHighWatermark > previousHighWatermark) {
  onHighWatermarkUpdated.accept(currentHighWatermark)
  previousHighWatermark = currentHighWatermark
}
```

This principle also applies to maintaining consistency between different data views - ensure that components have clear ownership of their state and that cross-component operations respect the logical data flow. Avoid moving functionality between components unless the data ownership boundaries are also properly adjusted.