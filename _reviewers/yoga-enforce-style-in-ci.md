---
title: Enforce style in CI
description: Configure automated formatting tools in CI/CD pipelines to enforce code
  style standards rather than silently fix violations. Use validation flags that cause
  the build to fail when formatting issues are detected, and ensure all commands run
  non-interactively.
repository: facebook/yoga
label: Code Style
language: Yaml
comments_count: 2
repository_stars: 18255
---

Configure automated formatting tools in CI/CD pipelines to enforce code style standards rather than silently fix violations. Use validation flags that cause the build to fail when formatting issues are detected, and ensure all commands run non-interactively.

For installation commands, always include flags to avoid user prompts:
```yaml
run: sudo apt-get install -y clang-format-${{ inputs.version }}
```

For formatting validation, use flags that check without modifying files and exit with error codes:
```yaml
run: npx --yes google-java-format --set-exit-if-changed --dry-run --glob=java/**/*.java
```

This approach catches style violations early in the development process and maintains consistent code formatting across the entire codebase by making compliance mandatory rather than optional.