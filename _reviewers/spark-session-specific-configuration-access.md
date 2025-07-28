---
title: Session-specific configuration access
description: Always access configuration through the appropriate session context rather
  than using global configuration access. This ensures that session-specific settings
  are respected and maintains consistency across different execution contexts.
repository: apache/spark
label: Configurations
language: Other
comments_count: 4
repository_stars: 41554
---

Always access configuration through the appropriate session context rather than using global configuration access. This ensures that session-specific settings are respected and maintains consistency across different execution contexts.

**Why this matters:**
- Different Spark sessions may have different configuration values
- Global configuration access can ignore session-specific overrides
- Proper session context ensures configuration consistency

**Preferred patterns:**

1. **Pass SQLConf instances explicitly:**
```scala
// Instead of accessing global config
val maxStringLen = SQLConf.get.getConf(SQLConf.JSON_MAX_STRING_LENGTH)

// Pass SQLConf instance to constructors
class JSONOptions(parameters: Map[String, String], sqlConf: SQLConf) {
  private val maxStringLen = sqlConf.getConf(SQLConf.JSON_MAX_STRING_LENGTH)
}
```

2. **Access config through SparkSession:**
```scala
// Instead of using global SQLConf.get
val shuffleCleanupMode = determineShuffleCleanupMode(SQLConf.get)

// Use session-specific configuration
val shuffleCleanupMode = determineShuffleCleanupMode(sparkSession.sessionState.conf)
```

3. **Use session timezone settings:**
```scala
// Instead of hardcoded UTC or assumptions
val zoneId = UTC

// Use session-specific timezone
val zoneId = DateTimeUtils.getZoneId(SQLConf.get.sessionLocalTimeZone)
```

This pattern follows established practices in components like `ParquetOptions` and ensures that configuration behavior is predictable and respects user-specified session settings.