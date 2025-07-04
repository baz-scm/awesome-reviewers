---
title: Property description conventions
description: 'When documenting configuration properties in Spring Boot applications,
  follow these conventions for clarity and consistency:


  1. Avoid starting descriptions with articles like "the" or "a"'
repository: spring-projects/spring-boot
label: Documentation
language: Java
comments_count: 5
repository_stars: 77637
---

When documenting configuration properties in Spring Boot applications, follow these conventions for clarity and consistency:

1. Avoid starting descriptions with articles like "the" or "a"
   ```java
   // INCORRECT:
   /** The max time to wait for the container to start. */
   
   // CORRECT:
   /** Time to wait for the container to start. */
   ```

2. Begin boolean property descriptions with "Whether..."
   ```java
   // INCORRECT:
   /** This signals to Brave that the propagation type... */
   
   // CORRECT:
   /** Whether the propagation type and tracing backend support sharing the span ID... */
   ```

3. Omit phrases like "by default" since defaults are processed separately
   ```java
   // INCORRECT:
   /** Sub-protocol to use in websocket handshake signature. Null by default. */
   
   // CORRECT:
   /** Sub-protocol to use in websocket handshake signature. */
   ```

4. Ensure all properties have descriptions that clearly explain their purpose
   ```java
   // INCORRECT:
   private final Map<String, Duration> expiry = new LinkedHashMap<>();
   
   // CORRECT:
   /**
    * Duration after which the value expires from the distribution.
    */
   private final Map<String, Duration> expiry = new LinkedHashMap<>();
   ```

5. Align descriptions with other similar properties in the same class for consistency

Following these conventions improves documentation readability and maintainability while providing a consistent experience for developers using your API.