---
title: Bean lifecycle management
description: When using containers and external services in Spring applications (especially
  with Testcontainers), declare them as Spring beans rather than static fields to
  ensure proper lifecycle management. This approach ensures that the application context
  will shut down clients first and then containers, preventing connection errors during
  shutdown.
repository: spring-projects/spring-boot
label: Spring
language: Other
comments_count: 2
repository_stars: 77637
---

When using containers and external services in Spring applications (especially with Testcontainers), declare them as Spring beans rather than static fields to ensure proper lifecycle management. This approach ensures that the application context will shut down clients first and then containers, preventing connection errors during shutdown.

For example, instead of:

```java
@TestConfiguration
class TestConfig {
    // Not recommended for services like Kafka, ActiveMQ, etc.
    private static final KafkaContainer kafka = new KafkaContainer();
    
    @Bean
    public KafkaClient kafkaClient() {
        return new KafkaClient(kafka.getBootstrapServers());
    }
}
```

Prefer:

```java
@TestConfiguration
class TestConfig {
    @Bean
    public KafkaContainer kafkaContainer() {
        return new KafkaContainer();
    }
    
    @Bean
    public KafkaClient kafkaClient(KafkaContainer container) {
        return new KafkaClient(container.getBootstrapServers());
    }
}
```

This pattern is especially important for messaging systems like ActiveMQ, Kafka, and Pulsar, where connection handling during shutdown is critical. The Spring container manages the lifecycle correctly, destroying client beans before container beans, which prevents errors caused by clients trying to access already-stopped services.