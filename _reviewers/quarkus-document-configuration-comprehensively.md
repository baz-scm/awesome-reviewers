---
title: Document configuration comprehensively
description: Configuration properties should be thoroughly documented with explicit
  details about constraints, units, default values, and behavior implications. This
  helps users understand how to use them correctly and troubleshoot issues.
repository: quarkusio/quarkus
label: Configurations
language: Java
comments_count: 7
repository_stars: 14667
---

Configuration properties should be thoroughly documented with explicit details about constraints, units, default values, and behavior implications. This helps users understand how to use them correctly and troubleshoot issues.

When documenting time-related properties, always specify the time unit and mention any rounding behavior:

```java
/**
 * The amount of time a client will wait until it closes the TCP connection after sending a close frame.
 * Note: This duration is rounded to the nearest second.
 */
Optional<Duration> closeTimeout();
```

For error messages related to configuration, make them actionable by mentioning the relevant configuration property:

```java
// Instead of:
return errorDataSet("The persistence unit datasource points to a non-allowed datasource");

// Better:
return errorDataSet("The persistence unit datasource points to a non-allowed datasource " +
        "(by default, only local databases are allowed). To allow remote databases, set quarkus.hibernate-orm.dev-ui.allowed-hosts=*");
```

Choose property names that follow consistent naming conventions and reflect their purpose clearly. For example, prefer `quarkus.rest-client.logging.scope` over `logLevel` to better express hierarchical relationships and maintain consistency with similar properties.

When deprecating configuration properties, provide clear migration paths with links to documentation:

```java
/**
 * @deprecated Use interfaces annotated with @ConfigMapping instead. 
 * See https://quarkus.io/guides/config-mappings for more info
 */
@Deprecated(since = "3.24", forRemoval = true)
```

For optional configuration, use Optional<> to avoid breaking changes when adding new properties:

```java
/**
 * Decrypt ID token.
 */
Optional<Boolean> decryptIdToken = Optional.empty();
```