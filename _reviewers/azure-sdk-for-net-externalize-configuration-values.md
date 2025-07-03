---
title: Externalize configuration values
description: Store configuration values (URLs, demands, pool names) in centralized
  variables rather than hardcoding them inline. This improves maintainability, ensures
  consistency across the codebase, and simplifies future updates. When possible, group
  related configurations in dedicated template files or variable groups.
repository: Azure/azure-sdk-for-net
label: Configurations
language: Yaml
comments_count: 4
repository_stars: 5809
---

Store configuration values (URLs, demands, pool names) in centralized variables rather than hardcoding them inline. This improves maintainability, ensures consistency across the codebase, and simplifies future updates. When possible, group related configurations in dedicated template files or variable groups.

Example:
```yaml
# Instead of:
pool:
  name: $(WINDOWSPOOL)
  demands: ImageOverride -equals $(WINDOWSVMIMAGE)

# Prefer:
pool:
  name: $(WINDOWSPOOL)
  demands: $(IMAGE_DEMAND)

variables:
  - name: IMAGE_DEMAND
    value: ImageOverride -equals $(WINDOWSVMIMAGE)
```

For API endpoints, pipeline definitions, and other configuration values that may change over time, always use variables rather than hardcoding values directly in scripts or pipeline definitions.
