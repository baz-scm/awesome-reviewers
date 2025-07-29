---
title: maintain naming consistency
description: Ensure consistent naming conventions and parameter ordering throughout
  the codebase. This includes maintaining consistent parameter order within classes,
  using established import aliases consistently, and ensuring method names accurately
  reflect their expected parameters and behavior.
repository: apache/kafka
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 30575
---

Ensure consistent naming conventions and parameter ordering throughout the codebase. This includes maintaining consistent parameter order within classes, using established import aliases consistently, and ensuring method names accurately reflect their expected parameters and behavior.

Key practices:
- Keep parameter ordering consistent within the same class or module (e.g., if other methods use `groupId` as the first parameter, maintain this pattern)
- Use established import aliases consistently instead of mixing full type names with aliases
- Ensure method names align with their actual parameters and usage context

Example of inconsistent parameter ordering:
```scala
// Other methods in class use groupId first
def fetchOffset(groupId: String, topic: String, partition: Int)

// This method breaks the pattern
def fetchOffset(topic: String, partition: Int, groupId: String) // Should reorder for consistency
```

Example of inconsistent alias usage:
```scala
// Import alias defined
import java.util.{Map => JMap}

// Inconsistent - mixing full name with available alias
def callback(responses: java.util.Map[TopicIdPartition, PartitionResponse])

// Consistent - use the established alias
def callback(responses: JMap[TopicIdPartition, PartitionResponse])
```

This consistency reduces cognitive load for developers and makes the codebase more maintainable.