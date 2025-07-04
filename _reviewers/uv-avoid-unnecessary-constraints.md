---
title: Avoid unnecessary constraints
description: 'When specifying dependencies and version requirements in project configuration
  files, avoid adding unnecessary constraints that could limit future compatibility.
  Unless there''s a specific known incompatibility issue:'
repository: astral-sh/uv
label: Configurations
language: Toml
comments_count: 2
repository_stars: 60322
---

When specifying dependencies and version requirements in project configuration files, avoid adding unnecessary constraints that could limit future compatibility. Unless there's a specific known incompatibility issue:

1. For Python packages in pyproject.toml, specify only the minimum required version rather than adding upper bounds:

```toml
# Preferred
requires-python = ">=3.11"

# Avoid unless necessary
requires-python = ">=3.11,<3.13"
```

2. For library crates in Cargo.toml, be selective about dependencies and consider whether they should be regular or development dependencies. Follow team standards for dependency management:

```toml
# Consider whether dependencies belong in [dependencies] or [dev-dependencies]
# Some dependencies like 'anyhow' should typically be avoided in library crates
```

This practice ensures your configurations remain flexible while still maintaining necessary compatibility requirements.