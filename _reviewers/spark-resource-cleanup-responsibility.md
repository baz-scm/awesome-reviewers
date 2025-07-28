---
title: Resource cleanup responsibility
description: Ensure proper resource management by clearly defining cleanup responsibilities
  and implementing robust cleanup patterns. Resources should be closed by their creator,
  and cleanup must occur even when exceptions happen during resource creation or usage.
repository: apache/spark
label: Error Handling
language: Other
comments_count: 4
repository_stars: 41554
---

Ensure proper resource management by clearly defining cleanup responsibilities and implementing robust cleanup patterns. Resources should be closed by their creator, and cleanup must occur even when exceptions happen during resource creation or usage.

Key principles:
1. **Creator responsibility**: The method that creates a resource should be responsible for its cleanup
2. **Comprehensive try-catch coverage**: Resource creation should be within try-catch blocks to handle failures
3. **Guaranteed cleanup**: Use finally blocks or try-with-resources to ensure cleanup happens even during exceptions
4. **Separate cleanup logic**: Implement dedicated cleanup methods with their own exception handling

Example pattern:
```scala
def fromJDBCConnectionFactory(getConnection: Int => Connection): JDBCDatabaseMetadata = {
  var conn: Connection = null
  
  def closeConnection(): Unit = {
    try {
      if (null != conn) {
        conn.close()
      }
    } catch {
      case e: Exception => logWarning("Exception closing connection during metadata fetch", e)
    }
  }
  
  try {
    conn = getConnection(-1)  // Resource creation in try block
    // ... use connection
  } catch {
    case NonFatal(e) =>
      logWarning("Exception while getting database metadata", e)
      // Return default values
  } finally {
    closeConnection()  // Guaranteed cleanup
  }
}
```

This prevents resource leaks and ensures graceful degradation when resource operations fail.