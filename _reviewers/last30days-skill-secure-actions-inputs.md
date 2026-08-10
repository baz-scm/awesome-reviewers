---
title: Secure Actions Inputs
description: 'In GitHub Actions, treat workflow inputs/expressions as potentially
  unsafe and follow two rules: (1) avoid interpolating `${{ ... }}` directly inside
  shell-script logic, and (2) do not persist Git credentials from `checkout`; instead,
  scope tokens to only the step that needs to push.'
repository: mvanhorn/last30days-skill
label: Security
language: Yaml
comments_count: 2
repository_stars: 57799
---

In GitHub Actions, treat workflow inputs/expressions as potentially unsafe and follow two rules: (1) avoid interpolating `${{ ... }}` directly inside shell-script logic, and (2) do not persist Git credentials from `checkout`; instead, scope tokens to only the step that needs to push.

Apply it like this:

- Injection-safe templating
  - Prefer passing values via `env:` and using normal shell variable expansion with proper quoting.
  - Example pattern:
    ```yaml
    - name: Create PR
      env:
        DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}
        VERSION: ${{ steps.prep.outputs.version }}
      run: |
        set -euo pipefail
        gh pr create \
          --base "${DEFAULT_BRANCH}" \
          --title "chore(release): bump version to ${VERSION}"
    ```

- Least-privilege credential handling
  - Disable persisted credentials on checkout:
    ```yaml
    - uses: actions/checkout@<pinned>
      with:
        fetch-depth: 0
        persist-credentials: false
    ```
  - For the push step, configure `origin` with the token only in that step (so other steps don’t inherit it).

This reduces risk of template-driven code injection and prevents unnecessary credential exposure in the workflow environment.