---
title: Use current configuration patterns
description: 'Always use the current recommended configuration patterns for your project,
  avoiding deprecated approaches. When configuring tests, features, or resource access:'
repository: elastic/elasticsearch
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 73104
---

Always use the current recommended configuration patterns for your project, avoiding deprecated approaches. When configuring tests, features, or resource access:

1. For test requirements, prefer capability-based specifications over version-based skipping:
```yaml
# Instead of:
requires:
  cluster_features: ["gte_v9.1.0"]
  
# Use:
requires:
  test_runner_features: [capabilities]
  capabilities:
    - method: DELETE
      path: /{index}/_block/{block}
```

2. For resource access configurations, be precise about paths and understand the available options:
```yaml
# Be specific with paths:
files:
  - relative_path_setting: "reindex.ssl.certificate"
  
# Consider whether glob patterns are appropriate:
files:
  - relative_path_setting: "reindex.ssl.*"
```

Using current configuration patterns improves maintainability, compatibility, and ensures the system behaves as expected across environments.
