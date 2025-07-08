---
title: Document dependency versioning
description: "Use consistent patterns for specifying dependency versions in configuration\
  \ files and document reasoning behind version constraints. \n\nGuidelines:\n1. Use\
  \ exact versions (`==`) for stability-critical dependencies"
repository: prowler-cloud/prowler
label: Configurations
language: Toml
comments_count: 3
repository_stars: 11834
---

Use consistent patterns for specifying dependency versions in configuration files and document reasoning behind version constraints. 

Guidelines:
1. Use exact versions (`==`) for stability-critical dependencies
2. Use version ranges only when there's a specific compatibility requirement
3. Document the reason for version constraints, especially when using ranges or preventing upgrades
4. Only add dependencies to the root configuration when the constraint applies project-wide

**Example:**
```toml
# Exact version for stability
some-critical-package = "1.2.3"

# Version range with documented reason
marshmallow = ">=3.15.0,<4.0.0"  # Safety tool incompatible with v4.0+

# Development dependency with more flexibility
pytest = ">=7.0.0"
```

When adding version constraints that differ from the project norm or prevent upgrades, add a comment explaining why, either in the PR description or inline with the configuration change.