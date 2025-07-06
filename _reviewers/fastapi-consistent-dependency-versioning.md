---
title: Consistent dependency versioning
description: When updating dependency version constraints in requirements files, ensure
  consistency with versions pinned by other dependencies in your project. Check what
  versions are used by major dependent packages before setting your own constraints
  to avoid compatibility issues.
repository: fastapi/fastapi
label: Configurations
language: Txt
comments_count: 2
repository_stars: 86871
---

When updating dependency version constraints in requirements files, ensure consistency with versions pinned by other dependencies in your project. Check what versions are used by major dependent packages before setting your own constraints to avoid compatibility issues.

For example, if a dependency like Starlette already pins a specific version range for a shared dependency:

```python
# Instead of setting arbitrary version constraints:
anyio[trio] >=3.2.1,<5.0.0

# Check what related packages require and align with them:
anyio[trio] >=3.6.2,<5.0.0  # Aligned with Starlette's requirements
```

This practice prevents dependency conflicts, reduces troubleshooting time, and ensures your configuration files maintain a coherent dependency strategy across the project.