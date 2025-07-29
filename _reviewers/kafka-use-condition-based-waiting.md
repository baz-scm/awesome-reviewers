---
title: Use condition-based waiting
description: Replace fixed-time delays with condition-based waiting mechanisms to
  ensure reliable synchronization and avoid timing-dependent race conditions. Fixed
  delays like `Thread.sleep()` are unreliable because they don't guarantee the expected
  state change has occurred, leading to flaky tests and potential production issues.
repository: apache/kafka
label: Concurrency
language: Other
comments_count: 3
repository_stars: 30575
---

Replace fixed-time delays with condition-based waiting mechanisms to ensure reliable synchronization and avoid timing-dependent race conditions. Fixed delays like `Thread.sleep()` are unreliable because they don't guarantee the expected state change has occurred, leading to flaky tests and potential production issues.

Instead of using arbitrary sleep durations, use proper waiting utilities that check for specific conditions:

```scala
// Avoid this - timing-based waiting
Thread.sleep(1000)
TimeUnit.MILLISECONDS.sleep(100)

// Prefer this - condition-based waiting  
TestUtils.waitUntilTrue(() => {
  brokers.head.metadataCache.getPartitionLeaderEndpoint(partition.topic, partition.partition(), listenerName).isDefined
}, "Metadata should be propagated")
```

This approach is more reliable because it waits for the actual condition to be met rather than assuming a fixed time is sufficient. It also makes tests faster when conditions are met quickly and prevents false failures when systems are under load.