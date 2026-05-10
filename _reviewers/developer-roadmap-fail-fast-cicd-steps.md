---
title: Fail-Fast CI/CD Steps
description: 'When building CI/CD pipelines, keep them scope-focused and deterministic,
  and add explicit quality gates so failures stop the deployment.


  Apply:

  - Put workflows in the conventional location and naming your team standard expects
  (e.g., `.github/workflows/main.yml`).'
repository: kamranahmedse/developer-roadmap
label: CI/CD
language: Markdown
comments_count: 5
repository_stars: 354523
---

When building CI/CD pipelines, keep them scope-focused and deterministic, and add explicit quality gates so failures stop the deployment.

Apply:
- Put workflows in the conventional location and naming your team standard expects (e.g., `.github/workflows/main.yml`).
- Keep the CI/CD goal minimal (avoid extra tooling/framework bootstraps when the purpose is learning/automation).
- Run formatting/validation before deployment (e.g., `terraform fmt` + `terraform validate`), and structure steps in a clear order (`init → plan → apply`-style).
- Ensure any step error fails the workflow and prevents deploy (default GitHub Actions behavior already stops on non-zero exit codes).

Example (GitHub Actions):
```yaml
name: CI/CD
on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Build/Test
        run: |
          echo "run tests/build here"

      - name: Validate (fail fast)
        run: |
          terraform fmt -check
          terraform validate

      - name: Deploy
        if: success()
        run: |
          terraform init
          terraform plan -out=tfplan
          terraform apply -auto-approve tfplan
```