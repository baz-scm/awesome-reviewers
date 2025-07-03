---
title: Limit token permissions
description: Always specify the minimum required permissions for the GITHUB_TOKEN
  in GitHub Actions workflows to enhance security. By default, the GITHUB_TOKEN has
  broad permissions that could potentially be exploited if a workflow is compromised.
repository: chef/chef
label: Security
language: Yaml
comments_count: 12
repository_stars: 7860
---

Always specify the minimum required permissions for the GITHUB_TOKEN in GitHub Actions workflows to enhance security. By default, the GITHUB_TOKEN has broad permissions that could potentially be exploited if a workflow is compromised.

Add an explicit permissions block at the workflow level or per job with only the necessary permissions:

```yaml
name: Verify

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

# Add a permissions block at the workflow level
permissions:
  contents: read
  # Only add other permissions as strictly needed

env:
  CHEF_LICENSE: accept-no-persist

jobs:
  linux-matrix:
    # Job configuration follows...
```

This practice follows the principle of least privilege and reduces the potential impact if a workflow is compromised by a malicious pull request or action.
