---
title: validate network state
description: Always validate network connectivity and cluster state before attempting
  network operations. Check for leader availability, partition existence, and proper
  metadata state to avoid unnecessary network calls and provide better error handling.
repository: apache/kafka
label: Networking
language: Java
comments_count: 3
repository_stars: 30575
---

Always validate network connectivity and cluster state before attempting network operations. Check for leader availability, partition existence, and proper metadata state to avoid unnecessary network calls and provide better error handling.

Key practices:
- Validate that partitions have leaders before performing operations
- Filter out partitions without leaders to avoid failed network requests
- Request metadata updates and flag partitions as awaiting updates when encountering network errors like NOT_LEADER_OR_FOLLOWER or FENCED_LEADER_EPOCH
- Separate validation of network state from the actual operation logic

Example from partition validation:
```java
// Check the partitions have leader
List<TopicPartition> partitionsWithoutLeader = filterNoneLeaderPartitions(partitionsToReset);
if (!partitionsWithoutLeader.isEmpty()) {
    String partitionStr = partitionsWithoutLeader.stream()
        .map(TopicPartition::toString)
        .collect(Collectors.joining(","));
    throw new LeaderNotAvailableException("The partitions \"" + partitionStr + "\" have no leader");
}

// Prepare data for partitions with leaders only
topicPartitions.removeAll(partitionsWithoutLeader);
```

Example from fetch error handling:
```java
if (partitionData.currentLeader().leaderId() != -1 && 
    partitionData.currentLeader().leaderEpoch() != -1) {
    // Process with valid leader info
    partitionsWithUpdatedLeaderInfo.put(partition, new Metadata.LeaderIdAndEpoch(...));
} else {
    // Request metadata update for invalid leader state
    requestMetadataUpdate(metadata, subscriptions, partition);
    subscriptions.awaitUpdate(partition);
}
```

This approach prevents wasted network calls, provides clearer error messages, and ensures operations only proceed when the network state is valid.