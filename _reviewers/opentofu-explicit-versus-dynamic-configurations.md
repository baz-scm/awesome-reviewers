---
title: Explicit versus dynamic configurations
description: Prefer explicit hardcoded configurations over dynamic ones when the configuration
  changes infrequently and control is important. While dynamic configurations (like
  API-driven or external service-based solutions) require less maintenance, explicit
  configurations provide better control and predictability.
repository: opentofu/opentofu
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 25901
---

Prefer explicit hardcoded configurations over dynamic ones when the configuration changes infrequently and control is important. While dynamic configurations (like API-driven or external service-based solutions) require less maintenance, explicit configurations provide better control and predictability.

For example, when configuring a CI workflow that needs to run against specific supported versions:

```yaml
strategy:
  matrix:
    include:
      - { branch: main }
      - { branch: v1.9 }
      - { branch: v1.8 }
      - { branch: v1.7 }
```

This approach might require occasional updates, but it provides complete control over which versions are included. To mitigate the maintenance burden, document the update process clearly in contribution guides, including when and how configurations should be updated (e.g., when releasing new versions or deprecating old ones).