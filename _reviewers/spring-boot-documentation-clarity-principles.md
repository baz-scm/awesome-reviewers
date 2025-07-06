---
title: Documentation clarity principles
description: 'When writing technical documentation, adhere to these core principles
  to ensure clarity and effectiveness:


  1. **Use precise technical terminology**: Choose the most accurate terms for technical
  concepts and be consistent with product names. Remove unnecessary qualifiers when
  context is clear.'
repository: spring-projects/spring-boot
label: Documentation
language: Other
comments_count: 6
repository_stars: 77637
---

When writing technical documentation, adhere to these core principles to ensure clarity and effectiveness:

1. **Use precise technical terminology**: Choose the most accurate terms for technical concepts and be consistent with product names. Remove unnecessary qualifiers when context is clear.

   ```adoc
   # Prefer
   This is especially useful for Container beans, as they keep their state despite the application restart.
   
   # Instead of
   This is especially useful for Testcontainer javadoc:org.testcontainers.containers.Container[] beans...
   ```

2. **Follow formatting conventions**: Use correct admonition formats (e.g., `NOTE` not `Note`), keep one sentence per line, and use idiomatic language.

   ```adoc
   # Prefer
   NOTE: The OpenTelemetry Logback appender and Log4j appender are not part of Spring Boot.
   You have to provide and configure them yourself.
   
   # Instead of
   Note: The OpenTelemetry Logback appender and Log4j appender are not part of Spring Boot. You have to provide and configure them yourself.
   ```

3. **Simplify when possible**: Document only recommended approaches rather than all possible variations to reduce cognitive load. When multiple approaches exist, clearly indicate the preferred method.

4. **Keep information current**: Regularly review and remove outdated information that no longer applies to current versions of the software.

5. **Use idiomatic language**: Choose proper prepositions and phrases that sound natural in technical contexts (e.g., "over HTTP" rather than "via HTTP" when discussing protocols).

Following these principles creates documentation that is more accessible, maintainable, and valuable to users.