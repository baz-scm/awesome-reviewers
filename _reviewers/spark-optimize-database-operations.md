---
title: optimize database operations
description: When working with database operations, prioritize batching multiple statements
  and pushing operations down to the database level for optimal performance. Use batch
  statements instead of executing individual prepared statements, and implement proper
  compatibility checks before attempting query pushdown optimizations.
repository: apache/spark
label: Database
language: Other
comments_count: 16
repository_stars: 41554
---

When working with database operations, prioritize batching multiple statements and pushing operations down to the database level for optimal performance. Use batch statements instead of executing individual prepared statements, and implement proper compatibility checks before attempting query pushdown optimizations.

For batching operations, group related database statements together:

```scala
// Instead of individual statements
conn.prepareStatement("CREATE TABLE test.people (name TEXT, id INTEGER)").executeUpdate()
conn.prepareStatement("INSERT INTO test.people VALUES ('fred', 1)").executeUpdate()
conn.prepareStatement("INSERT INTO test.people VALUES ('mary', 2)").executeUpdate()

// Use batch operations
val batchStmt = conn.createStatement()
batchStmt.addBatch("CREATE TABLE test.people (name TEXT, id INTEGER)")
batchStmt.addBatch("INSERT INTO test.people VALUES ('fred', 1)")
batchStmt.addBatch("INSERT INTO test.people VALUES ('mary', 2)")
batchStmt.executeBatch()
```

For join pushdown optimizations, ensure proper compatibility validation before attempting to push operations to the database:

```scala
override def isOtherSideCompatibleForJoin(other: SupportsPushDownJoin): Boolean = {
  if (!jdbcOptions.pushDownJoin || !dialect.supportsJoin) return false
  
  other.isInstanceOf[JDBCScanBuilder] &&
    jdbcOptions.url == other.asInstanceOf[JDBCScanBuilder].jdbcOptions.url
}
```

This approach reduces network round trips, improves query execution performance, and leverages database-native optimizations. Always validate compatibility and feature support before implementing pushdown operations to avoid runtime failures.