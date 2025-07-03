---
title: Centralize pipeline configurations
description: Use centralized templates and variables for pipeline configurations instead
  of duplicating or hardcoding values. This improves maintainability, ensures consistency,
  and makes platform-specific adaptations easier to manage.
repository: Azure/azure-sdk-for-net
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 5809
---

Use centralized templates and variables for pipeline configurations instead of duplicating or hardcoding values. This improves maintainability, ensures consistency, and makes platform-specific adaptations easier to manage.

Key practices:
1. Reference existing templates from `/eng/pipelines/templates/` instead of creating duplicates
2. Include the image variables template `/eng/pipelines/templates/variables/image.yml` in pipelines that reference VM images
3. Use pool variables (LINUXPOOL, WINDOWSPOOL, MACPOOL) for pool names
4. Use demand-based configuration for Windows/Linux and vmImage pattern for Mac

Example:
```yaml
# Good practice
variables:
  - template: /eng/pipelines/templates/variables/image.yml

jobs:
  - job: BuildAndTest
    pool:
      name: $(WINDOWSPOOL)
      demands: $(WindowsImageDemand)
```

Instead of:
```yaml
# Avoid this approach
jobs:
  - job: BuildAndTest
    pool:
      name: azsdk-pool-mms-win-2022-general
      vmImage: windows-2022
```

This approach makes it easier to update image configurations across all pipelines and supports platform-specific configuration patterns.
