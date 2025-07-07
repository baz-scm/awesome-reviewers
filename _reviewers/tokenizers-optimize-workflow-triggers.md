---
title: Optimize workflow triggers
description: Configure CI workflows with targeted triggers and path filters to balance
  thoroughness with efficiency. Run critical build jobs on every commit for affected
  components, while avoiding unnecessary builds when changes don't impact certain
  components.
repository: huggingface/tokenizers
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 9868
---

Configure CI workflows with targeted triggers and path filters to balance thoroughness with efficiency. Run critical build jobs on every commit for affected components, while avoiding unnecessary builds when changes don't impact certain components.

For example, use path filters to only run specific workflows when relevant files change:

```yaml
name: Node Build
on:
  push:
    paths:
      - 'bindings/node/**'
      - 'src/**'
    paths-ignore:
      - '*.md'
      - 'docs/**'
  pull_request:
    paths:
      - 'bindings/node/**'
      - 'src/**'

jobs:
  build:
    # Build configuration here
```

Keep your CI components updated to their latest stable versions:
```yaml
- name: Install Python
  uses: actions/setup-python@v5  # Use latest stable version
```

Consider workflow organization - separate workflows by component or purpose, but look for opportunities to consolidate setup steps and reuse configuration across similar jobs.