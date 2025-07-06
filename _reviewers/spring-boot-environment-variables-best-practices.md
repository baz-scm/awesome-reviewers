---
title: Environment variables best practices
description: 'When working with environment variables in configuration files, follow
  these practices to ensure reliability and testability:


  1. Use placeholder syntax `${ENV_VAR}` to reference environment variables in both
  properties and YAML configuration files'
repository: spring-projects/spring-boot
label: Configurations
language: Other
comments_count: 2
repository_stars: 77637
---

When working with environment variables in configuration files, follow these practices to ensure reliability and testability:

1. Use placeholder syntax `${ENV_VAR}` to reference environment variables in both properties and YAML configuration files
2. Provide default values using the `${ENV_VAR:default-value}` syntax to ensure the application functions even when environment variables are not set
3. For testing environment variable-dependent code, design components to accept injectable Map objects rather than using reflection-based libraries

Example of proper environment variable usage in YAML:

```yaml
environments:
  dev:
    url: ${DEV_ENV_URL}
    name: ${DEV_ENV_NAME:development-environment}
```

When testing code that depends on environment variables, prefer dependency injection instead of reflection:

```java
// Instead of using reflection-based libraries to modify System.getenv()
public class ConfigReader {
    private final Map<String, String> env;
    
    // For production use
    public ConfigReader() {
        this(System.getenv());
    }
    
    // For testing use
    public ConfigReader(Map<String, String> env) {
        this.env = env;
    }
    
    public String getConfig(String key, String defaultValue) {
        return env.getOrDefault(key, defaultValue);
    }
}
```