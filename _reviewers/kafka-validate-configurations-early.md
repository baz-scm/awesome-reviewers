---
title: Validate configurations early
description: Perform comprehensive configuration validation as early as possible in
  the execution flow, before any state modifications occur. This prevents invalid
  configurations from causing partial state changes and ensures cleaner error handling.
repository: apache/kafka
label: Configurations
language: Other
comments_count: 3
repository_stars: 30575
---

Perform comprehensive configuration validation as early as possible in the execution flow, before any state modifications occur. This prevents invalid configurations from causing partial state changes and ensures cleaner error handling.

Key principles:
1. **Validate before state changes**: Check all configuration constraints before modifying any formatter state, creating resources, or initializing components
2. **Account for all relevant flags**: When validating configurations, consider all related configuration flags that might affect validity (e.g., `unstable.feature.versions.enable` affecting which metadata versions are allowed)
3. **Provide context-aware error messages**: Include information about which configurations are actually supported based on current settings

Example from StorageTool validation:
```scala
// Validate configuration conflicts early, before formatter modifications
if (!config.quorumConfig.voters().isEmpty &&
  (namespace.getString("initial_controllers") != null || namespace.getBoolean("standalone"))) {
  // Fail fast with clear error message
  throw new InvalidConfigurationException("Cannot use --initial-controllers or --standalone with static quorum")
}

// Later, when handling version parsing, account for configuration flags
try {
  formatter.setReleaseVersion(MetadataVersion.fromVersionString(releaseVersion))
} catch {
  case _: Throwable =>
    val supportedVersions = if (config.unstableFeatureVersionsEnabled) {
      // Include unstable versions in error message
      metadataVersionsToString(MetadataVersion.MINIMUM_VERSION, MetadataVersion.latest())
    } else {
      metadataVersionsToString(MetadataVersion.MINIMUM_VERSION, MetadataVersion.latestProduction())
    }
    throw new TerseFailure(s"Unknown metadata.version $releaseVersion. Supported versions: $supportedVersions")
}
```

This approach prevents partial failures, reduces debugging complexity, and provides users with actionable error messages that reflect their actual configuration context.