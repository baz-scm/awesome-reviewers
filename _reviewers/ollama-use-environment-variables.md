---
title: Use environment variables
description: Use environment variables instead of hardcoding configuration values
  such as file paths, port numbers, or system-specific locations. This makes the code
  more flexible across different platforms, installation methods, and user preferences.
repository: ollama/ollama
label: Configurations
language: Go
comments_count: 5
repository_stars: 145704
---

Use environment variables instead of hardcoding configuration values such as file paths, port numbers, or system-specific locations. This makes the code more flexible across different platforms, installation methods, and user preferences.

When implementing configuration:

1. Use environment variables for values that might differ between environments
2. Provide sensible defaults when environment variables are not set
3. Support platform-specific path conventions (like `~` expansion) across operating systems
4. Handle architecture differences (x86_64, aarch64, etc.) appropriately

Example:

```go
// Bad: Hardcoded path that won't work across environments
func RegisterService() {
    server, err = zeroconf.Register(
        "OllamaInstance",    // Service Name
        "_ollama._tcp",      // Service Type
        "local.",            // Domain
        11434,               // Port - hardcoded!
    )
}

// Good: Use environment variable with fallback
func RegisterService() {
    port := 11434 // Default
    if hostEnv := os.Getenv("OLLAMA_HOST"); hostEnv != "" {
        if _, portStr, err := net.SplitHostPort(hostEnv); err == nil && portStr != "" {
            if p, err := strconv.Atoi(portStr); err == nil {
                port = p
            }
        }
    }
    
    server, err = zeroconf.Register(
        "OllamaInstance",    // Service Name
        "_ollama._tcp",      // Service Type
        "local.",            // Domain
        port,                // Port from environment or default
    )
}
```

For path handling, support platform-specific conventions:

```go
func getConfigPath() string {
    if path, exists := os.LookupEnv("OLLAMA_CONFIG"); exists {
        // Handle home directory expansion
        if strings.HasPrefix(path, "~/") {
            homeDir, err := os.UserHomeDir()
            if err == nil {
                path = filepath.Join(homeDir, path[2:])
            }
        }
        return path
    }
    // Default fallback
    homeDir, _ := os.UserHomeDir()
    return filepath.Join(homeDir, ".ollama", "config")
}
```