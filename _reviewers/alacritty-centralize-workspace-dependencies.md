---
title: centralize workspace dependencies
description: Define shared dependencies at the workspace level in the root Cargo.toml
  to ensure version consistency and prevent conflicts across the project. This approach
  centralizes dependency management and makes it easier to maintain uniform versions
  throughout the codebase.
repository: alacritty/alacritty
label: Configurations
language: Toml
comments_count: 2
repository_stars: 59675
---

Define shared dependencies at the workspace level in the root Cargo.toml to ensure version consistency and prevent conflicts across the project. This approach centralizes dependency management and makes it easier to maintain uniform versions throughout the codebase.

When multiple crates in your workspace use the same dependency, declare it in the workspace dependencies section and reference it from individual crates. This prevents version mismatches and reduces the risk of using unmaintained or conflicting dependency versions.

Example:
```toml
# Root Cargo.toml
[workspace.dependencies]
toml = "0.9.2"
toml_edit = "0.23.1"
dirs = "2.0"  # Use consistent version across workspace

# Individual crate Cargo.toml
[dependencies]
toml = { workspace = true }
dirs = { workspace = true }
```

This practice is especially important when dealing with dependencies that have breaking changes between major versions or when some dependencies are unmaintained and you need to stick with specific stable versions across your entire workspace.