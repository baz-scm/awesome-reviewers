---
title: Explicit version constraints
description: Always specify explicit version constraints for dependencies in configuration
  files (like pyproject.toml), particularly when dealing with Python version compatibility.
  Use conditional dependencies based on Python versions to handle compatibility issues,
  and include explanatory comments when adding constraints.
repository: apache/airflow
label: Configurations
language: Toml
comments_count: 4
repository_stars: 40858
---

Always specify explicit version constraints for dependencies in configuration files (like pyproject.toml), particularly when dealing with Python version compatibility. Use conditional dependencies based on Python versions to handle compatibility issues, and include explanatory comments when adding constraints.

For example:
```
# Python 3 saml is not compatible with Python 3.13 yet, so we pin it
"python3-saml>=1.16.0; python_version < \"3.13\"",

# Specify different versions for different Python versions
"pandas>=2.1.2; python_version < \"3.13\"",
"pandas>=2.3.0; python_version >= \"3.13\"",
```

This practice prevents build failures due to incomplete package metadata, especially when working with lowest compatible versions or when dependencies don't proactively specify Python version exclusions. Use an optimistic approach for upper bounds unless tests specifically indicate incompatibility.