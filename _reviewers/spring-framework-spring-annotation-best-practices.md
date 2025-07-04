---
title: Spring annotation best practices
description: 'When working with Spring annotations, follow these guidelines to avoid
  common issues:


  1. **Use interface types for dependency injection**: When autowiring dependencies,
  declare fields using the interface type rather than the implementation class. This
  ensures proper behavior with proxies and AOP.'
repository: spring-projects/spring-framework
label: Spring
language: Other
comments_count: 4
repository_stars: 58382
---

When working with Spring annotations, follow these guidelines to avoid common issues:

1. **Use interface types for dependency injection**: When autowiring dependencies, declare fields using the interface type rather than the implementation class. This ensures proper behavior with proxies and AOP.

```java
// RECOMMENDED
@Autowired
private Pojo self;  // Interface type

// AVOID (unless you're certain CGLIB proxies are being used)
@Autowired
private SimplePojo self;  // Implementation type
```

2. **Remember @Bean flexibility**: Methods annotated with `@Bean` can be defined in any `@Component`-annotated class, not just in `@Configuration` classes.

3. **Avoid annotation-based injection in infrastructure classes**: Do not use `@Autowired`, `@Inject`, or `@Resource` annotations within BeanFactory implementations or their dependencies. This can cause `BeanCurrentlyInCreationException` due to initialization timing issues. Use programmatic lookups instead for these infrastructure components.

Following these practices will help prevent subtle runtime errors and improve the maintainability of your Spring applications.