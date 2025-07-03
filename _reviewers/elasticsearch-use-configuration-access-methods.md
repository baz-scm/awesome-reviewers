---
title: Use configuration access methods
description: When accessing configuration settings, always use the appropriate type-safe
  accessor methods provided by the configuration framework rather than manual string
  parsing. This improves code readability, maintainability, and reduces potential
  bugs from string parsing errors.
repository: elastic/elasticsearch
label: Configurations
language: Java
comments_count: 6
repository_stars: 73104
---

When accessing configuration settings, always use the appropriate type-safe accessor methods provided by the configuration framework rather than manual string parsing. This improves code readability, maintainability, and reduces potential bugs from string parsing errors.

For boolean settings:
- Use `getAsBoolean()` with explicit default values instead of `Boolean.parseBoolean()`
- For system properties, use `Booleans.parseBoolean()` with default value

For example, instead of:
```java
boolean sourceOnly = Boolean.parseBoolean(indexSettings.getSettings().get("index.source_only"));
boolean isFrozen = Boolean.parseBoolean(writeIndex.getSettings().get("index.frozen"));
boolean enabledDebugLogs = Boolean.parseBoolean(System.getProperty(ENABLE_KERBEROS_DEBUG_LOGS_KEY));
```

Prefer:
```java
boolean sourceOnly = indexSettings.getAsBoolean("index.source_only", false);
boolean isFrozen = writeIndex.getSettings().getAsBoolean("index.frozen", false);
boolean enabledDebugLogs = Booleans.parseBoolean(System.getProperty(ENABLE_KERBEROS_DEBUG_LOGS_KEY), false);
```

Similarly, when exposing configuration parameters in APIs, avoid implicit defaults and require explicit parameters. When checking compatibility or validating configurations, use clear and readable expressions that make the intent obvious.

This practice promotes consistency, makes default values explicit, and leverages the built-in validation provided by the configuration framework.
