---
title: Environment variable validation
description: Always validate environment variables and provide appropriate fallbacks
  when using them for configuration. Environment variables should be checked for existence
  and non-empty values before use, with clear fallback behavior defined.
repository: docker/compose
label: Configurations
language: Go
comments_count: 8
repository_stars: 35858
---

Always validate environment variables and provide appropriate fallbacks when using them for configuration. Environment variables should be checked for existence and non-empty values before use, with clear fallback behavior defined.

When reading environment variables, use proper validation patterns:

```go
// Good: Check for existence and non-empty value
if cacheHome := os.Getenv("XDG_CACHE_HOME"); cacheHome != "" {
    base = cacheHome
} else {
    // Provide clear fallback
    base = filepath.Join(os.Getenv("HOME"), ".cache")
}

// Good: Use flag defaults from environment variables
func addProjectFlags(cmd *cobra.Command) {
    cmd.Flags().StringVar(&progressMode, "progress", 
        getEnvOrDefault("COMPOSE_PROGRESS", "auto"), 
        "Set type of progress output")
}
```

For experimental features, use descriptive environment variable names with clear prefixes:
```go
if _, ok := os.LookupEnv("COMPOSE_EXPERIMENTAL_INCLUDE_REMOTE"); ok {
    // Enable experimental feature
}
```

Establish clear precedence rules for configuration sources (command line flags > environment variables > config files > defaults) and document the expected behavior when multiple sources are present. Always handle the case where environment variables might be set but empty, as this often indicates intentional override behavior.