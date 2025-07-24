---
title: explicit configuration management
description: Make all configuration settings explicit and well-documented, avoiding
  implicit defaults and auto-detection where possible. This includes dependency versions,
  build flags, environment variables, and tool configurations.
repository: docker/compose
label: Configurations
language: Other
comments_count: 7
repository_stars: 35858
---

Make all configuration settings explicit and well-documented, avoiding implicit defaults and auto-detection where possible. This includes dependency versions, build flags, environment variables, and tool configurations.

Key principles:
- **Be conservative with updates**: Only update minimum required versions when absolutely necessary, as noted: "list the minimum required version, and only update if it's impossible to use with older versions"
- **Make implicit settings explicit**: Set configuration values explicitly rather than relying on defaults (e.g., `GO111MODULE=on`, `CGO_ENABLED=0`)
- **Document temporary configurations**: When using workarounds like replace rules, clearly document why they exist and when they can be removed
- **Prefer simple defaults over complex auto-detection**: Use simple defaults with override capability rather than complex detection logic

Example of explicit configuration in Makefile:
```makefile
# Explicit module and CGO settings
GO111MODULE=on
CGO_ENABLED=0

# Simple default with override capability  
BUILDX_CMD ?= docker buildx

# Clear documentation for temporary workarounds
replace (
    // reverts https://github.com/moby/buildkit/pull/4094 to fix fsutil issues on Windows
    github.com/docker/buildx => github.com/crazy-max/buildx v0.8.1-0.20240130141015-d7042ae5516c
)
```

This approach reduces surprises, makes builds more reproducible, and helps maintainers understand the reasoning behind configuration choices.