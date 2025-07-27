---
title: Use centralized configuration access
description: Always access configuration values through the configuration object rather
  than direct helper functions or environment variables. This ensures consistent behavior
  across the application and provides proper abstraction from the underlying value
  sources.
repository: snyk/cli
label: Configurations
language: Go
comments_count: 4
repository_stars: 5178
---

Always access configuration values through the configuration object rather than direct helper functions or environment variables. This ensures consistent behavior across the application and provides proper abstraction from the underlying value sources.

Instead of calling utility functions directly or accessing environment variables, use the configuration object to retrieve values. This approach decouples the implementation from knowing where values come from and how they need to be named, making the code more maintainable and testable.

Example of what to avoid:
```go
// Don't use helper functions directly
tmpDirectory := utils.GetTemporaryDirectory(cacheDirectory, cliVersion)

// Don't access environment variables directly  
integration := os.Getenv("SNYK_INTEGRATION_NAME")
```

Preferred approach:
```go
// Use configuration object instead
tmpDirectory := config.GetString(configuration.TEMP_DIR_PATH)

// Access through configuration abstraction
integration := globalConfiguration.GetString(configuration.INTEGRATION_NAME)
```

This pattern ensures that configuration values are consistently accessed, properly validated, and can be easily mocked or overridden for testing. It also enables centralized configuration management where alternative keys and default values can be handled uniformly.