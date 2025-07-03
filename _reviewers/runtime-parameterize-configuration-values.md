---
title: Parameterize configuration values
description: Extract hard-coded configuration values into variables, parameters, or
  templates to improve reusability and simplify maintenance. When the same value is
  used in multiple places or might need to change in the future, define it once and
  reference it throughout your configuration files.
repository: dotnet/runtime
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 16578
---

Extract hard-coded configuration values into variables, parameters, or templates to improve reusability and simplify maintenance. When the same value is used in multiple places or might need to change in the future, define it once and reference it throughout your configuration files.

Examples:
1. For build scripts with multiple parameters:
```yaml
# Instead of:
- script: make run TARGET_ARCH=arm64 DEPLOY_AND_RUN=false RUNTIME_FLAVOR=CoreCLR STATIC_LINKING=true

# Use:
- script: make run TARGET_ARCH=${{ parameters.targetArch }} DEPLOY_AND_RUN=${{ parameters.deployAndRun }} RUNTIME_FLAVOR=${{ parameters.runtimeFlavor }} STATIC_LINKING=${{ parameters.staticLinking }}
```

2. For repeated configuration values:
```yaml
# Define once:
variables:
  timeoutPerTestCollection: 180

# Reference where needed:
jobParameters:
  timeoutInMinutes: ${{ variables.timeoutPerTestCollection }}
```

This practice reduces duplication, centralizes configuration management, and makes future updates more efficient and less error-prone.
