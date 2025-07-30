---
title: Python version standardization
description: Establish and document a consistent Python version standard for dependency
  compilation across the project. Team confusion about which Python version to use
  for pip-compile leads to build inconsistencies, compatibility issues, and wasted
  development time.
repository: Unstructured-IO/unstructured
label: Configurations
language: Txt
comments_count: 2
repository_stars: 12117
---

Establish and document a consistent Python version standard for dependency compilation across the project. Team confusion about which Python version to use for pip-compile leads to build inconsistencies, compatibility issues, and wasted development time.

The discussions reveal conflicting approaches: some team members believe dependencies should be compiled with the minimum supported Python version (3.9) for maximum compatibility, while others use different versions (3.10). This inconsistency causes build failures and requires rework.

**Implementation:**
1. Document the official Python version for pip-compile in your project's README or contributing guidelines
2. Add version checks to your Makefile or build scripts to prevent compilation with incorrect Python versions
3. Include the Python version requirement in CI/CD pipeline documentation

**Example from the discussions:**
```
# Error when wrong Python version is used:
AssertionError
python version not equal to expected 3.9: Python 3.10.13
make: *** [pip-compile] Error 1
```

Ensure all team members understand and follow the same Python version standard to maintain build reproducibility and avoid compatibility issues across different environments.