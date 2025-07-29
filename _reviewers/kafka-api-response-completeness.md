---
title: API response completeness
description: Ensure API responses contain all necessary data fields and provide mechanisms
  for clients to verify operation results. When building API responses, successful
  operations should include complete metadata (such as topic IDs, timestamps, or other
  identifiers), while failed operations should contain appropriate error information.
  Additionally, provide...
repository: apache/kafka
label: API
language: Other
comments_count: 2
repository_stars: 30575
---

Ensure API responses contain all necessary data fields and provide mechanisms for clients to verify operation results. When building API responses, successful operations should include complete metadata (such as topic IDs, timestamps, or other identifiers), while failed operations should contain appropriate error information. Additionally, provide corresponding read/list operations that allow clients to verify the results of write operations.

For example, when implementing delete operations like `deleteShareGroupOffsets`, ensure that:
1. Successful responses include all relevant identifiers
2. A corresponding list operation (`listShareGroupOffsets`) exists for verification
3. Response builders properly merge successful and failed parts without losing critical data

```scala
// Ensure topic IDs are preserved in successful responses
val responseBuilder = new AlterShareGroupOffsetsResponse.Builder()
// For successful topics, include topic ID in response
responseBuilder.addPartition(topic.topicName(), partition.partitionIndex(), error.error)
// Verify merge operation preserves all necessary fields
requestHelper.sendMaybeThrottle(request, responseBuilder.merge(response).build())
```

This practice enables clients to implement robust error handling and verification workflows, improving the overall reliability of API interactions.