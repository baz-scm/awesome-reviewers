---
title: validate configuration dependencies
description: Validate configuration dependencies and constraints at initialization
  time rather than allowing invalid combinations to cause runtime failures. When configurations
  have interdependencies, implement validation logic that checks these relationships
  early and provides clear error messages.
repository: apache/kafka
label: Configurations
language: Java
comments_count: 4
repository_stars: 30575
---

Validate configuration dependencies and constraints at initialization time rather than allowing invalid combinations to cause runtime failures. When configurations have interdependencies, implement validation logic that checks these relationships early and provides clear error messages.

Key practices:
- Validate configuration constraints in the config class itself (e.g., `KafkaConfig` should validate that `quorum.auto.join.enable` is only true when `process.role` contains `controller`)
- Use appropriate validation methods like `CommandLineUtils.checkRequiredArgs()` but delegate validation to specialized methods when possible
- For test configurations, ensure resource requirements match the test scenario (e.g., use 2 brokers with appropriate replica settings rather than over-provisioning with 5 brokers)
- When handling feature configurations, validate that finalized feature levels are consistent with the current image rather than making assumptions about missing features

Example from the discussions:
```java
// In KafkaConfig validation
public static final String QUORUM_AUTO_JOIN_ENABLE = QUORUM_PREFIX + "auto.join.enable";
public static final boolean DEFAULT_QUORUM_AUTO_JOIN_ENABLE = false;

// Validation should ensure this is only true when process.role contains controller
if (autoJoinEnabled && !processRoles.contains("controller")) {
    throw new ConfigException("quorum.auto.join.enable can only be true when process.role contains controller");
}
```

This approach prevents configuration-related runtime errors and makes system requirements explicit and discoverable during setup rather than during operation.