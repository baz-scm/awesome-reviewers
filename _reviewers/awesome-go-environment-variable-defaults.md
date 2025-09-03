---
title: Environment variable defaults
description: Configuration values should be externalized to environment variables
  with sensible defaults to avoid hard-coding values in source code. This approach
  improves flexibility, security, and maintainability by allowing different configurations
  across environments without code changes.
repository: avelino/awesome-go
label: Configurations
language: Go
comments_count: 2
repository_stars: 151435
---

Configuration values should be externalized to environment variables with sensible defaults to avoid hard-coding values in source code. This approach improves flexibility, security, and maintainability by allowing different configurations across environments without code changes.

When accessing configuration through environment variables, always provide appropriate fallback values to ensure the application functions correctly even when optional environment variables are not set.

Example implementation:
```go
var (
    githubApiAuthorizationToken = os.Getenv("GITHUB_API_TOKEN")
    userAgent = getEnvWithDefault("USER_AGENT", "MyApp/1.0")
)

func getEnvWithDefault(key, defaultValue string) string {
    if value := os.Getenv(key); value != "" {
        return value
    }
    return defaultValue
}

// Usage in HTTP request
request.Header.Set("User-Agent", userAgent)
```

This pattern ensures that sensitive values like API tokens can be injected at runtime while maintaining reasonable defaults for non-sensitive configuration like user agent strings.