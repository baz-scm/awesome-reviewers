---
title: validate environment variables early
description: Environment variables should be validated early in the application lifecycle
  with descriptive, actionable error messages. Use specific, namespaced variable names
  to avoid conflicts in CI/CD environments and other systems. When possible, avoid
  hardcoding configuration values and instead use configuration files or well-defined
  environment variables.
repository: snyk/cli
label: Configurations
language: Other
comments_count: 3
repository_stars: 5178
---

Environment variables should be validated early in the application lifecycle with descriptive, actionable error messages. Use specific, namespaced variable names to avoid conflicts in CI/CD environments and other systems. When possible, avoid hardcoding configuration values and instead use configuration files or well-defined environment variables.

For required environment variables, implement early validation checks that fail fast with clear guidance on what the user needs to do:

```go
// Good: Early validation with descriptive error
if iacRulesURL := os.Getenv("IAC_RULES_URL"); iacRulesURL == "" {
    return fmt.Errorf("IAC_RULES_URL environment variable is required. Please set it to the appropriate rules bundle URL")
}
```

Avoid generic environment variable names that could conflict with system or CI/CD variables:

```makefile
# Avoid: Generic name that could conflict
ifeq ($(DEBUG), 1)

# Better: Use namespaced/specific names
ifeq ($(SNYK_DEBUG_BUILD), 1)
```

When configuration values are needed across multiple environments, prefer configuration files over hardcoded values:

```makefile
# Avoid: Hardcoded version
$(PKG) -t node16-alpine-x64 -o $(OUTPUT)

# Better: Use configuration file
NODE_VERSION = $(shell cat .nvmrc | cut -d'v' -f2 | cut -d'.' -f1)
$(PKG) -t node$(NODE_VERSION)-alpine-x64 -o $(OUTPUT)
```