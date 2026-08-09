---
title: Workflow least-privilege
description: 'When writing GitHub Actions workflows, apply security best practices
  for (1) permissions scope and (2) trust boundaries around PR data.


  **1) Use least-permissive permissions**'
repository: apple/container
label: Security
language: Yaml
comments_count: 2
repository_stars: 48787
---
{% raw %}
When writing GitHub Actions workflows, apply security best practices for (1) permissions scope and (2) trust boundaries around PR data.

**1) Use least-permissive permissions**
- Set top-level `permissions` to the minimum required (or empty), and grant any extra rights at the **job level**, not globally.

**2) Treat PR data as untrusted**
- Before passing PR-derived inputs to actions, confirm the action does not read untrusted code/configuration from the PR (e.g., labeler rules/config).
- Prefer rules/configuration stored in the trusted repository state (e.g., `main`) over anything coming from the PR/artefacts.

**Example pattern**
```yml
permissions: {}

jobs:
  create-labels:
    runs-on: ubuntu-latest
    permissions:
      issues: write

    steps:
      - uses: actions/labeler@v6
        with:
          # PR-derived identifiers are OK if the action only analyzes diffs
          # but ensure label rules/config are not taken from untrusted PR content.
          pr-number: ${{ inputs.pr_number }}
```

If an action’s behavior around PR-provided config is unclear, verify in documentation/source or constrain the workflow so trusted configuration is used.
{% endraw %}
