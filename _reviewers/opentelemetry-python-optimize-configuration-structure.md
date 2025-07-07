---
title: Optimize configuration structure
description: Structure configuration files like tox.ini to maximize maintainability
  and efficiency. Use factor prefixes (e.g., "test-opentelemetry:", "lint:") to install
  packages only for specific environments, avoiding unnecessary dependencies. When
  naming environments, avoid characters that have special meaning in the tool (e.g.,
  use "precommit" instead of...
repository: open-telemetry/opentelemetry-python
label: Configurations
language: Other
comments_count: 5
repository_stars: 2061
---

Structure configuration files like tox.ini to maximize maintainability and efficiency. Use factor prefixes (e.g., "test-opentelemetry:", "lint:") to install packages only for specific environments, avoiding unnecessary dependencies. When naming environments, avoid characters that have special meaning in the tool (e.g., use "precommit" instead of "pre-commit" since tox treats hyphens as factor separators).

Example:
```ini
[testenv]
deps =
  -c dev-requirements.txt
  # Install specific packages only for lint environments
  lint: -r lint-requirements.txt
  # Install specific packages only for test environments
  test-opentelemetry: pytest
  test-opentelemetry: pytest-benchmark
```

This approach reduces test environment setup time and makes dependencies explicit for each environment type. Consider using tools like pip-sync to keep environments in sync with requirements.txt changes. For complex projects, evaluate whether specialized requirements files for different virtual environments improve clarity or add unnecessary complexity.