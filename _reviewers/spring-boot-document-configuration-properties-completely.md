---
title: Document configuration properties completely
description: Configuration properties should be fully documented with clear descriptions,
  explicit default values, and proper metadata. This helps users understand and configure
  the application correctly.
repository: spring-projects/spring-boot
label: Configurations
language: Java
comments_count: 6
repository_stars: 77637
---

Configuration properties should be fully documented with clear descriptions, explicit default values, and proper metadata. This helps users understand and configure the application correctly.

Key requirements:
- Provide explicit default values in the property definition
- Include short, simple property descriptions without Javadoc tags
- Add enum defaults to additional-spring-configuration-metadata.json
- Use consistent property naming within property groups

Example:
```java
@ConfigurationProperties("spring.example")
public class ExampleProperties {
    /**
     * Maximum number of connections to create.
     */
    private int maxConnections = 100;
    
    /**
     * Connection timeout duration.
     */
    private Duration timeout = Duration.ofSeconds(30);
    
    // Getters/setters
}
```

For enums:
```json
{
  "properties": [
    {
      "name": "spring.example.mode",
      "defaultValue": "auto"
    }
  ]
}
```