---
title: Secure Workflow Permissions
description: 'Apply two security practices to GitHub Actions workflows:


  1) Enforce least privilege

  - Set `permissions: {}` at the workflow level (or default deny) and only add the
  minimal scopes required for each job/step.'
repository: redis/redis
label: Security
language: Yaml
comments_count: 2
repository_stars: 74261
---

Apply two security practices to GitHub Actions workflows:

1) Enforce least privilege
- Set `permissions: {}` at the workflow level (or default deny) and only add the minimal scopes required for each job/step.

2) Safely pass dynamic workflow data into shell
- Values coming from `needs.*.outputs` (e.g., tag/version strings) should not be interpolated repeatedly into shell snippets.
- Instead, pass them through a controlled job-level environment variable (or a dedicated setup step) and always quote them when used in bash/script invocations.

Example pattern:
```yml
permissions: {}

jobs:
  extract-release-info:
    # ...

  create-tarball:
    needs: extract-release-info
    runs-on: ubuntu-latest
    env:
      RELEASE_TAG: ${{ needs.extract-release-info.outputs.tag_name }}

    steps:
      - name: Create tarball
        run: |
          echo "Creating tarball for version ${RELEASE_TAG}..."
          # If using a script, pass quoted args:
          # ./utils/releasetools/01_create_tarball.sh "${RELEASE_TAG}"
```
This reduces blast radius (least privilege) and mitigates shell-injection risk when dynamic workflow outputs are consumed by bash.