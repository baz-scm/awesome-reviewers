---
title: Structured log message quality
description: Design log messages to be clear, concise, and properly structured to
  maximize their utility for debugging and monitoring. When using structured logging,
  configure reasonable limits for data complexity to prevent resource exhaustion and
  ensure logs remain usable.
repository: spring-projects/spring-boot
label: Logging
language: Java
comments_count: 2
repository_stars: 77637
---

Design log messages to be clear, concise, and properly structured to maximize their utility for debugging and monitoring. When using structured logging, configure reasonable limits for data complexity to prevent resource exhaustion and ensure logs remain usable.

Key practices:
1. Set appropriate limits for structured logging depth (prefer lower values like 32 instead of excessively high values like 1000) to prevent both stack overflow and log storage issues.
2. Consolidate related log messages when possible to improve readability and reduce log noise.
3. Provide context in log messages to make them self-contained and meaningful.

Example of consolidated logging (preferred):
```java
if (dataSourceList.size() == 1) {
    logger.info("H2 console available at '{}'. Database '{}' available at '{}'", 
                path, dataSourceList.get(0).getName(), connectionUrl);
} else {
    logger.info("H2 console available at '{}'", path);
    dataSourceList.forEach(ds -> 
        logger.info("Database '{}' available at '{}'", ds.getName(), ds.getUrl()));
}
```

Instead of separate log messages:
```java
logger.info("H2 console available at '" + path + "'.");
dataSource.orderedStream().forEachOrdered((available) -> {
    try (Connection connection = available.getConnection()) {
        logger.info("Database available at '" + connection.getMetaData().getURL() + "'");
    }
    // ...
});
```