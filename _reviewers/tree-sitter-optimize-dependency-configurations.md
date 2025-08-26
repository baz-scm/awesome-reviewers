---
title: optimize dependency configurations
description: When configuring dependencies in package manifests, prioritize efficiency
  and maintainability by avoiding redundant dependencies, using flexible versioning,
  and explicitly managing features. Before adding new dependencies, check if existing
  ones already provide the required functionality. Use version ranges (like "^1.0")
  instead of exact pins to allow...
repository: tree-sitter/tree-sitter
label: Configurations
language: Toml
comments_count: 3
repository_stars: 21799
---

When configuring dependencies in package manifests, prioritize efficiency and maintainability by avoiding redundant dependencies, using flexible versioning, and explicitly managing features. Before adding new dependencies, check if existing ones already provide the required functionality. Use version ranges (like "^1.0") instead of exact pins to allow compatible updates while maintaining stability. When configuring features, disable defaults when not needed and explicitly specify required features for better control.

Example from Cargo.toml:
```toml
# Good: Use existing dependency instead of adding new one
dirs = "3.0"  # Already provides home_dir functionality

# Good: Flexible versioning for compatibility  
cc = "^1.0"

# Good: Explicit feature management
regex = { version = "1.10.4", default-features = false, features = ["perf", "unicode"] }
```

This approach reduces dependency bloat, improves build reliability, and makes version management more predictable across different environments.