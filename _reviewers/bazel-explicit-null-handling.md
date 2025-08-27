---
title: Explicit null handling
description: Always make null handling explicit through proper annotations, defensive
  checks, and clear documentation. Use @Nullable annotations for parameters and fields
  that can be null, add precondition checks with meaningful error messages for required
  non-null values, and document when and why values may be null.
repository: bazelbuild/bazel
label: Null Handling
language: Java
comments_count: 6
repository_stars: 24489
---

Always make null handling explicit through proper annotations, defensive checks, and clear documentation. Use @Nullable annotations for parameters and fields that can be null, add precondition checks with meaningful error messages for required non-null values, and document when and why values may be null.

For nullable parameters and fields, use @Nullable annotations with explanatory comments:
```java
@Nullable
private final String mnemonic; // null if not yet known

public void maybeReportSubcommand(Spawn spawn, @Nullable String spawnRunner) {
  // method implementation
}
```

For required non-null parameters, use defensive precondition checks that include the problematic value in error messages:
```java
public ExecutionInfo(Map<String, String> requirements, String execGroup) {
  this.executionInfo = ImmutableMap.copyOf(requirements);
  this.execGroup = checkNotNull(execGroup, "execGroup cannot be null");
}

// Pass the input to checkNotNull for better error context
FileArtifactValue metadata = checkNotNull(metadataSupplier.getMetadata(input), input);
```

Document null behavior in javadoc, especially for return values:
```java
/**
 * Returns the action result from cache.
 * @return the cached result, or null if not found in cache
 */
@Nullable
public abstract ActionResult actionResult();
```

This approach prevents null-related bugs by making null contracts explicit and providing clear failure points when null constraints are violated.