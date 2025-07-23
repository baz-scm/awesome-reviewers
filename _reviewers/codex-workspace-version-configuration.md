---
title: Workspace version configuration
description: Standardize version management across multi-crate Rust projects by using
  workspace versioning. This reduces duplication and ensures consistency across all
  crates in your project.
repository: openai/codex
label: Configurations
language: Toml
comments_count: 2
repository_stars: 31275
---

Standardize version management across multi-crate Rust projects by using workspace versioning. This reduces duplication and ensures consistency across all crates in your project.

Implementation:
1. Define the version once in the workspace Cargo.toml:
```toml
[workspace]
version = "0.1.0"
```

2. Reference this version in each crate's Cargo.toml:
```toml
[package]
name = "your-crate-name"
version = { workspace = true }
```

This approach centralizes version management, making it easier to release coordinated updates across all crates while maintaining a consistent configuration structure.