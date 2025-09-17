---
title: workspace dependency consistency
description: All internal project dependencies should use workspace configuration
  instead of direct path or git references to ensure consistent versioning and build
  behavior across the monorepo. Maintain the standard `{ workspace = true }` syntax
  format and avoid redundant configuration options when using workspace dependencies.
repository: unionlabs/union
label: Configurations
language: Toml
comments_count: 4
repository_stars: 74800
---

All internal project dependencies should use workspace configuration instead of direct path or git references to ensure consistent versioning and build behavior across the monorepo. Maintain the standard `{ workspace = true }` syntax format and avoid redundant configuration options when using workspace dependencies.

When adding new internal dependencies, always check if they can be configured in the workspace root and referenced consistently. Avoid specifying `default-features = false` or other options that may conflict with workspace-level configuration.

Example of correct workspace dependency usage:
```toml
[dependencies]
# Correct - uses workspace configuration
ibc-events = { workspace = true }
unionlabs = { workspace = true }

# Incorrect - direct path reference
# ibc-events = { version = "0.1.0", path = "../ibc-events" }

# Incorrect - direct git reference  
# sui_sdk = { git = "https://github.com/mystenlabs/sui", package = "sui-sdk" }

# Incorrect - redundant configuration with workspace
# unionlabs = { workspace = true, default-features = false }
```

This approach centralizes dependency management, reduces configuration drift, and ensures all modules use compatible versions of shared dependencies.