---
title: Consistent observability data
description: When implementing observability features, always ensure consistency in
  your data model, especially with tags and attributes. This helps prevent issues
  with backends that expect consistent tag sets.
repository: spring-projects/spring-boot
label: Observability
language: Java
comments_count: 7
repository_stars: 77637
---

When implementing observability features, always ensure consistency in your data model, especially with tags and attributes. This helps prevent issues with backends that expect consistent tag sets.

1. **Use consistent tag sets across metrics**: Always include the same set of tag keys for metrics of the same type, even when some values are missing.

2. **Provide defaults for missing values**: Use standardized defaults like "unknown" or "N/A" rather than omitting tags when values are unavailable.

```java
// INCORRECT: Inconsistent tag sets
Gauge.builder("git.info", () -> 1L)
    .tag("branch", props.getBranch()) // May be omitted if null
    .tag("id", props.getShortCommitId())
    .register(registry);

// CORRECT: Consistent tag sets with defaults
Gauge.builder("git.info", () -> 1L)
    .tag("branch", props.getBranch() != null ? props.getBranch() : "unknown")
    .tag("id", props.getShortCommitId() != null ? props.getShortCommitId() : "unknown")
    .register(registry);
```

3. **Document metrics clearly**: Use descriptive names that indicate what's being measured and from which perspective:

```java
// INCORRECT: Ambiguous description
builder.description("Duration of requests made to HTTP Server")

// CORRECT: Clear perspective
builder.description("Duration of HTTP server request handling")
```

4. **Be explicit about propagation behavior**: When configuring trace context propagation, explicitly define extraction order and format preferences to ensure reliable tracing across service boundaries.

These practices help avoid issues with observability backends (like Prometheus) that may not handle inconsistent tag sets well and improve the overall reliability and usability of your observability data.