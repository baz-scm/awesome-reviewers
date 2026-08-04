---
title: CI coverage and scope
description: 'When changing CI/CD (and related policy configs), ensure your pipeline
  enforces the expected scope end-to-end: correct review routing, test/version coverage,
  and validation against the full change set.'
repository: Azure/azure-cli
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 4592
---

When changing CI/CD (and related policy configs), ensure your pipeline enforces the expected scope end-to-end: correct review routing, test/version coverage, and validation against the full change set.

Apply these rules:
1) Route to the correct team in policy/config
- If a config expects a team, don’t use a label or non-team identifier.
- Example:
  - Bad: `reviewer: act-codegen-extensibility-squad`
  - Good: `reviewer: Azure/act-codegen-extensibility-squad`

2) Keep test matrices aligned to the official-release version set
- Don’t “spray” multiple versions unless they’re explicitly part of the supported/release matrix.
- Example approach: remove extra Python version entries and keep only the release-tested set (e.g., “RPM build: 3.12; everything else: 3.14”).

3) Run validation against the full diff range (avoid last-commit-only checks)
- For non-PR runs, diff only `HEAD~1` can miss multi-commit pushes.
- Use the default branch (or another stable baseline) as the target so all new changes are included.
- Example:
  - Bad: `python scripts/ci/check_aliases_source_url.py --src=HEAD --tgt=HEAD~1`
  - Good: `python scripts/ci/check_aliases_source_url.py --src=HEAD --tgt=origin/dev` (or your default branch).