---
title: avoid overly specific examples
description: When documenting configuration options, use generic examples that don't
  unnecessarily tie documentation to specific versions, environments, or exact default
  values. This keeps documentation maintainable and prevents examples from becoming
  outdated or environment-specific.
repository: apache/kafka
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 30575
---

When documenting configuration options, use generic examples that don't unnecessarily tie documentation to specific versions, environments, or exact default values. This keeps documentation maintainable and prevents examples from becoming outdated or environment-specific.

Instead of specifying exact OS versions or precise default values:
```bash
# Too specific
image_name="ducker-ak-openjdk:17-buster" bash tests/docker/run_tests.sh

# Better - generic version
image_name="ducker-ak-openjdk:17" bash tests/docker/run_tests.sh
```

For default values, mention their existence without being overly specific:
```
You can customize the OpenJDK base image using the `-j` or `--jdk` parameter, otherwise a default value will be used.
```

This approach makes configuration documentation more resilient to changes and easier to maintain across different environments.