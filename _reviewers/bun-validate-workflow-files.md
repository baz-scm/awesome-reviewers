---
title: Validate workflow files
description: 'Ensure all CI/CD workflow configuration files are validated for accuracy
  and consistency. Small errors in workflow files can prevent automation from triggering
  correctly or cause unexpected behavior. Pay special attention to:'
repository: oven-sh/bun
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 79093
---

Ensure all CI/CD workflow configuration files are validated for accuracy and consistency. Small errors in workflow files can prevent automation from triggering correctly or cause unexpected behavior. Pay special attention to:

1. File extension consistency between actual files and path triggers
2. Correct property names according to the platform's documentation

**Examples of common issues:**

Incorrect path trigger (file extension mismatch):
```yaml
on:
  pull_request:
    paths:
      - ".github/workflows/bun-release-test.yml" # Wrong: actual file has .yaml extension
```

Correct path trigger:
```yaml
on:
  pull_request:
    paths:
      - ".github/workflows/bun-release-test.yaml" # Matches the actual file extension
```

Incorrect property name:
```yaml
- name: Create Pull Request
  uses: peter-evans/create-pull-request@v3
  with:
    lables: "automation" # Wrong: 'lables' is a typo
```

Correct property name:
```yaml
- name: Create Pull Request
  uses: peter-evans/create-pull-request@v3
  with:
    labels: "automation" # Correct property name
```

Consider implementing a validation step in your workflow development process to catch these issues early.