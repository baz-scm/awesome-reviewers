---
title: Pin dependency versions
description: Always use exact version pinning (==) for dependencies in requirements
  files rather than version ranges. This ensures build reproducibility and prevents
  unexpected behavior when dependencies release new versions.
repository: open-telemetry/opentelemetry-python
label: Configurations
language: Txt
comments_count: 4
repository_stars: 2061
---

Always use exact version pinning (==) for dependencies in requirements files rather than version ranges. This ensures build reproducibility and prevents unexpected behavior when dependencies release new versions.

For dependencies that must work across multiple Python versions, identify a compatible version that works for all supported Python versions rather than using version ranges. This approach prevents compatibility issues like the one seen with pre-commit, where newer versions dropped support for Python 3.8.

If conditional dependencies are needed, still use fixed versions in the conditionals.

```
# Good
importlib-metadata==6.11.0
pre-commit==3.5.0  # Compatible with all supported Python versions

# Avoid
importlib-metadata<9.0.0
importlib-metadata<=8.2.0
```

Additionally, maintain consistency by using the same version of a dependency throughout the entire repository. This prevents subtle bugs that can occur when different components use different versions of the same library.

This approach ensures consistent behavior across all development and CI environments, improving reproducibility and reducing debugging time.