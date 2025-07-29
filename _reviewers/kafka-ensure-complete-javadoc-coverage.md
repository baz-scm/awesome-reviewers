---
title: Ensure complete JavaDoc coverage
description: 'All public classes, methods, and parameters must have comprehensive
  JavaDoc documentation. This includes:


  1. **Class-level JavaDoc**: Every public class and interface requires JavaDoc explaining
  its purpose and usage'
repository: apache/kafka
label: Documentation
language: Java
comments_count: 4
repository_stars: 30575
---

All public classes, methods, and parameters must have comprehensive JavaDoc documentation. This includes:

1. **Class-level JavaDoc**: Every public class and interface requires JavaDoc explaining its purpose and usage
2. **Method JavaDoc**: All public methods need documentation describing their behavior, parameters, return values, and exceptions
3. **Parameter documentation**: When adding new parameters to existing methods, always include @param tags in the JavaDoc
4. **Deprecated elements**: When marking code as @Deprecated, use plain `@Deprecated` annotation without metadata and add corresponding `@deprecated` JavaDoc tag with version and replacement information

Example for deprecated code:
```java
/**
 * @deprecated Since 4.2 and should not be used any longer.
 * @see org.apache.kafka.streams.StreamsConfig
 */
@Deprecated
public class BrokerNotFoundException {
    // implementation
}
```

Example for new parameters:
```java
/**
 * Creates a new RecordAccumulator instance.
 * @param logContext the log context
 * @param batchSize the batch size
 * @param kafka19012Instrumentation instrumentation for KAFKA-19012 metrics
 */
public RecordAccumulator(LogContext logContext, 
                        int batchSize,
                        Kafka19012Instrumentation kafka19012Instrumentation) {
    // implementation
}
```

This ensures consistent documentation standards and helps maintain code readability and API usability for both internal developers and external users.