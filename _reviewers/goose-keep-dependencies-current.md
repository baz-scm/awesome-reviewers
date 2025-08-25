---
title: Keep dependencies current
description: Always use the latest stable versions of dependencies in configuration
  files like Cargo.toml, and avoid deprecated or unmaintained packages. Outdated dependencies
  can introduce security vulnerabilities, compatibility issues, and technical debt.
repository: block/goose
label: Configurations
language: Toml
comments_count: 2
repository_stars: 19037
---

Always use the latest stable versions of dependencies in configuration files like Cargo.toml, and avoid deprecated or unmaintained packages. Outdated dependencies can introduce security vulnerabilities, compatibility issues, and technical debt.

When reviewing dependency changes:
- Check if newer stable versions are available (e.g., updating opentelemetry from "0.27" to "0.30")
- Verify that dependencies are actively maintained and not deprecated
- Replace deprecated packages with maintained alternatives (e.g., serde_yaml is deprecated and should be replaced)
- Use tooling like the VS Code 'crates' extension to identify version updates

Example of problematic dependency management:
```toml
# Outdated - current version is 0.30
opentelemetry = "0.27"

# Deprecated package
serde_yaml = "0.9"

# Outdated - current version is 0.30  
jsonschema = "0.18"
```

Make dependency version reviews a standard part of configuration file changes to maintain a healthy and secure codebase.