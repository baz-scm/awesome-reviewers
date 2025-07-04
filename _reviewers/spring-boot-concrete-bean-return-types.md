---
title: Concrete bean return types
description: When defining `@Bean` methods in Spring configurations, use concrete
  return types rather than interfaces while using interface types in `@ConditionalOnMissingBean`
  annotations. This approach maximizes type information available to the Spring bean
  factory while maintaining flexibility in bean overriding.
repository: spring-projects/spring-boot
label: Spring
language: Java
comments_count: 6
repository_stars: 77637
---

When defining `@Bean` methods in Spring configurations, use concrete return types rather than interfaces while using interface types in `@ConditionalOnMissingBean` annotations. This approach maximizes type information available to the Spring bean factory while maintaining flexibility in bean overriding.

For example, instead of:

```java
@Bean
@ConditionalOnMissingBean
PulsarConsumerFactory<?> pulsarConsumerFactory(PulsarClient pulsarClient) {
    return new DefaultPulsarConsumerFactory<>(/* parameters */);
}
```

Prefer:

```java
@Bean
@ConditionalOnMissingBean(PulsarConsumerFactory.class)
DefaultPulsarConsumerFactory<?> pulsarConsumerFactory(PulsarClient pulsarClient) {
    return new DefaultPulsarConsumerFactory<>(/* parameters */);
}
```

This provides Spring with precise type details during bean creation while allowing applications to override the bean with any implementation of the interface. The bean factory will have more complete information about the actual implementation, which helps with autowiring, debugging, and type safety throughout the application context.