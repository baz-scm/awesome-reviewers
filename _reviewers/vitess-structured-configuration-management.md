---
title: Structured configuration management
description: Avoid using global configuration singletons that rely on string-based
  lookups, as they lead to brittle code that's hard to maintain. Instead, implement
  a structured approach where configuration values are explicitly declared with their
  types, sources (flags, environment variables, config files), and default values.
  This improves compile-time safety,...
repository: vitessio/vitess
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 19815
---

Avoid using global configuration singletons that rely on string-based lookups, as they lead to brittle code that's hard to maintain. Instead, implement a structured approach where configuration values are explicitly declared with their types, sources (flags, environment variables, config files), and default values. This improves compile-time safety, documentation, and maintainability.

For dynamic configurations that can be reloaded at runtime, ensure thread-safety and consider performance implications. When implementing config reloading, handle invalid configurations gracefully by logging errors and maintaining the last valid configuration rather than crashing.

Example:

```go
// BAD: Global, string-based configuration
func doSomething() {
    name := viper.GetString("name") // Brittle, no type safety
    fmt.Println(name)
}

// GOOD: Structured, type-safe configuration
var (
    configKey = viperutil.KeyPrefixFunc("myapp")
    
    // Explicitly declare configuration with sources
    accountName = viperutil.Configure(
        configKey("account.name"),
        viperutil.Options[string]{
            EnvVars:  []string{"MY_APP_ACCOUNT_NAME"},
            FlagName: "account_name",
            Default:  "",
            Dynamic:  false, // Static config loaded only at startup
        },
    )
)

// Register flags and bind them to config values
func registerFlags(fs *pflag.FlagSet) {
    fs.String("account_name", accountName.Default(), "Account name for the application")
    viperutil.BindFlags(fs, accountName)
}

// Use the configuration value
func doSomething() {
    name := accountName.Get()
    fmt.Println(name)
}
```