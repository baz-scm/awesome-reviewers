---
title: Ensure dependency compatibility
description: When adding or updating dependencies in configuration files (Pipfile,
  requirements.txt), ensure compatibility with all supported Python versions in the
  project. Generated lock files and specific version constraints should work with
  the minimum supported Python version to prevent CI failures or production issues.
repository: bridgecrewio/checkov
label: Configurations
language: Other
comments_count: 2
repository_stars: 7668
---

When adding or updating dependencies in configuration files (Pipfile, requirements.txt), ensure compatibility with all supported Python versions in the project. Generated lock files and specific version constraints should work with the minimum supported Python version to prevent CI failures or production issues.

Example:
```
# If your project supports Python 3.8+, avoid dependencies like:
asteval = "==1.0.6"  # This version may not support Python 3.8

# Instead use:
asteval = "<1.0.6"  # Or a version known to be compatible with Python 3.8+
```

When generating lock files, use the minimum supported Python version environment to ensure all CI jobs and production environments can install dependencies successfully. Before committing changes to dependency configurations, verify compatibility by testing with the lowest supported Python version.