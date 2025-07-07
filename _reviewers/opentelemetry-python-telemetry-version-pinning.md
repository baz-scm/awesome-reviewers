---
title: Telemetry version pinning
description: When specifying observability frameworks like OpenTelemetry in requirements
  files, use the compatible release operator (~=) with only the major and minor version
  numbers, omitting the patch version. This ensures you receive bug fixes in patch
  releases while protecting against potential breaking changes in minor versions.
repository: open-telemetry/opentelemetry-python
label: Observability
language: Txt
comments_count: 2
repository_stars: 2061
---

When specifying observability frameworks like OpenTelemetry in requirements files, use the compatible release operator (~=) with only the major and minor version numbers, omitting the patch version. This ensures you receive bug fixes in patch releases while protecting against potential breaking changes in minor versions.

Example:
```
# Recommended
opentelemetry-api~=1.25

# Not recommended
opentelemetry-api>=1.25.0
opentelemetry-api~=1.25.0
```

This approach balances stability with bug fixes for your observability stack, ensuring consistent telemetry collection across environments.