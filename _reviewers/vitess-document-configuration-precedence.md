---
title: Document configuration precedence
description: When implementing multiple configuration methods (e.g., config files,
  command-line flags, environment variables), clearly document the precedence order
  and warn users about potential conflicts. Unclear precedence rules can lead to unexpected
  system behavior and difficult troubleshooting.
repository: vitessio/vitess
label: Configurations
language: Txt
comments_count: 2
repository_stars: 19815
---

When implementing multiple configuration methods (e.g., config files, command-line flags, environment variables), clearly document the precedence order and warn users about potential conflicts. Unclear precedence rules can lead to unexpected system behavior and difficult troubleshooting.

For example, if command-line flags override config file settings (or vice versa), this relationship should be explicitly stated in documentation. Consider adding runtime warnings when potentially conflicting configuration methods are detected:

```go
// Example of warning about conflicting configuration methods
if configFileProvided && legacyConfigFlagProvided {
    log.Warning("Both --config-file and --legacy-config flags detected. " +
                "Values from --legacy-config will take precedence over config file values. " +
                "Please migrate to using only --config-file as --legacy-config is deprecated.")
}
```

When introducing new configuration approaches, mark older methods as deprecated with clear migration instructions to help users transition smoothly. This helps maintain backward compatibility while encouraging adoption of improved configuration patterns.