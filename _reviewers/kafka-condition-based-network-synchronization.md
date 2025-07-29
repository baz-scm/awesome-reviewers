---
title: condition-based network synchronization
description: When waiting for network state propagation or distributed system synchronization,
  avoid using fixed sleep times and instead implement condition-based waiting that
  verifies the actual desired state. Fixed delays are unreliable in network environments
  due to variable latency and don't guarantee the expected state has been reached.
repository: apache/kafka
label: Networking
language: Other
comments_count: 2
repository_stars: 30575
---

When waiting for network state propagation or distributed system synchronization, avoid using fixed sleep times and instead implement condition-based waiting that verifies the actual desired state. Fixed delays are unreliable in network environments due to variable latency and don't guarantee the expected state has been reached.

Instead of using arbitrary sleep durations:
```scala
def sleepMillisToPropagateMetadata(durationMs: Long, partition: TopicPartition): Unit = {
  Thread.sleep(durationMs)  // Unreliable - doesn't verify actual state
}
```

Implement condition-based waiting that polls for the actual desired network state:
```scala
def waitForMetadataPropagation(brokers: Seq[Broker], partition: TopicPartition): Unit = {
  TestUtils.waitUntilTrue(() => {
    brokers.forall(broker => 
      getPartitionLeader(broker, partition) == expectedLeader
    )
  }, "Metadata propagation across all brokers")
}
```

This approach ensures reliable synchronization by verifying that all network nodes have reached the expected state, rather than assuming a fixed time duration is sufficient for network propagation.