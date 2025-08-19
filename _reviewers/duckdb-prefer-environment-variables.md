---
title: prefer environment variables
description: When configuring behavior that needs to work across different execution
  contexts (CI workflows, manual runs, different build systems), prefer environment
  variables over command-line flags or hardcoded options. Environment variables provide
  broader compatibility and can be easily overridden without modifying scripts or
  commands.
repository: duckdb/duckdb
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 32061
---

When configuring behavior that needs to work across different execution contexts (CI workflows, manual runs, different build systems), prefer environment variables over command-line flags or hardcoded options. Environment variables provide broader compatibility and can be easily overridden without modifying scripts or commands.

Additionally, ensure all environment variables are properly defined and have clear dependencies. Avoid referencing undefined variables or creating confusing variable chains.

Example:
```yaml
# Instead of hardcoded command-line flags:
run: build/reldebug/test/unittest --force-reload --force-storage --summarize-failures

# Prefer environment variables that can be read by the application:
env:
  SUMMARIZE_FAILURES: 1
run: build/reldebug/test/unittest --force-reload --force-storage

# Ensure variables are properly defined:
env:
  ENABLE_EXTENSION_AUTOLOADING: 1  # Clear, defined value
  # Not: ENABLE_EXTENSION_AUTOLOADING: ${{ inputs.undefined_variable }}
```

This approach makes configuration more flexible and allows the same settings to work with different execution methods like `make allunit` or direct test execution.