---
title: Configuration documentation clarity
description: Ensure configuration documentation clearly and accurately describes environment
  variables, command-line flags, and their relationships. Pay special attention to
  precedence rules, equivalent options, and proper grammar when explaining configuration
  behavior.
repository: docker/compose
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 35858
---

Ensure configuration documentation clearly and accurately describes environment variables, command-line flags, and their relationships. Pay special attention to precedence rules, equivalent options, and proper grammar when explaining configuration behavior.

Key areas to review:
- Verify environment variable names and their effects are correctly documented
- Clearly explain relationships between environment variables and command-line flags
- Document precedence rules (e.g., command-line flags override environment variables)
- Use consistent and grammatically correct language when describing configuration options

Example of good documentation:
```yaml
# Clear precedence explanation
Setting the `COMPOSE_PROJECT_NAME` environment variable is equivalent to the `-p` flag,
and `COMPOSE_PROFILES` environment variable is equivalent to the `--profiles` flag.

If a flag is set via the command line, the associated environment variable is ignored.
```

This ensures developers understand exactly how different configuration methods interact and which takes precedence in various scenarios.