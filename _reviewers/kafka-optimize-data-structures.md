---
title: optimize data structures
description: When working with data structures and collections, optimize for performance
  and correctness by using modern APIs, proper sizing, result filtering, and lazy
  initialization. Use `List.of()` and `Map.of()` instead of legacy `Collections.singletonList()`
  and `Collections.singletonMap()` for better readability and performance. Size collections
  appropriately -...
repository: apache/kafka
label: Database
language: Java
comments_count: 4
repository_stars: 30575
---

When working with data structures and collections, optimize for performance and correctness by using modern APIs, proper sizing, result filtering, and lazy initialization. Use `List.of()` and `Map.of()` instead of legacy `Collections.singletonList()` and `Collections.singletonMap()` for better readability and performance. Size collections appropriately - avoid initializing with zero capacity when you know elements will be added. Filter results to match input parameters when reusing cached data to prevent returning unrelated entries. Delay object creation until all required parameters are available to avoid unnecessary work and ensure data consistency.

Example of modern collection usage:
```java
// Instead of:
Collections.singletonList(new StreamsGroupSubtopologyDescription(...))
Collections.singletonMap(groupId, future)

// Use:
List.of(new StreamsGroupSubtopologyDescription(...))
Map.of(groupId, future)
```

Example of proper collection sizing and lazy initialization:
```java
// Instead of creating objects early with incomplete data:
new FetchRequest.PartitionData(topicId, offset, 0, 0, ...)

// Delay creation until maxBytes is known:
// Collect required data first, then create objects with complete parameters
```

This approach improves performance, reduces memory allocation overhead, and ensures data consistency - critical factors for database operations and data access patterns.