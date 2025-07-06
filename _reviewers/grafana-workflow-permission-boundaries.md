---
title: Workflow permission boundaries
description: Always define explicit and minimal permission boundaries in GitHub Actions
  workflows to adhere to the principle of least privilege. By default, workflows have
  broad permissions that could be exploited if compromised. Specify permissions at
  either the workflow or job level to restrict the GITHUB_TOKEN to only required access
  levels.
repository: grafana/grafana
label: Security
language: Yaml
comments_count: 2
repository_stars: 68825
---

Always define explicit and minimal permission boundaries in GitHub Actions workflows to adhere to the principle of least privilege. By default, workflows have broad permissions that could be exploited if compromised. Specify permissions at either the workflow or job level to restrict the GITHUB_TOKEN to only required access levels.

Example:
```yaml
name: Example Workflow

# Recommended: Set permissions at workflow level
permissions:
  # Start with minimal permissions
  contents: read
  # Add other permissions only as needed:
  # issues: write
  # pull-requests: write

jobs:
  example-job:
    runs-on: ubuntu-latest
    # Alternatively, set permissions at job level
    # permissions:
    #   contents: read
    steps:
      - uses: actions/checkout@v4
      # Job steps
```

This approach prevents potential security breaches by limiting the access scope of workflow runs, reducing the impact of supply chain attacks or compromised dependencies.