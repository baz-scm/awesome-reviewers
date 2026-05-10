---
title: CI workflow correctness
description: 'All CI workflows must be syntactically valid, reliably triggered, and
  logically non-redundant.


  Apply these rules:

  1) Every step must be valid: each `- name:` entry must include either `uses:` or
  `run:` (never both missing).'
repository: TheAlgorithms/Python
label: CI/CD
language: Yaml
comments_count: 12
repository_stars: 220912
---

All CI workflows must be syntactically valid, reliably triggered, and logically non-redundant.

Apply these rules:
1) Every step must be valid: each `- name:` entry must include either `uses:` or `run:` (never both missing).
2) Condition + command belong together: put `if:` on the same step as the `run:` (or `uses:`).
3) Triggers must match the repo: ensure the referenced branches in `on: push` / `on: pull_request` actually exist; avoid `paths-ignore` patterns that skip directories containing code.
4) Version pinning clarity: when pinning a GitHub Action to a commit SHA, the inline comment must match the intended release version.
5) Avoid duplicate work: don’t rerun linters/tests already covered by dedicated lint/test workflows or pre-commit jobs.
6) Respect project runtime policy: don’t hardcode an older Python version if the project expects testing against the latest production CPython; align job installs with the intended uv dependency groups.

Example (valid conditional step):
```yaml
- name: Build docs artifact
  if: ${{ success() }}
  run: |
    scripts/build_directory_md.py 2>&1 | tee DIRECTORY.md
```
Example (pin comment matches intent):
```yaml
- name: Set up uv
  uses: astral-sh/setup-uv@37802adc94f370d6bfd71619e3f0bf239e1f3b78 # v7.6.0
```
Example (sanity on triggers):
- Only ignore files/directories if they truly contain no executable/code paths required for CI, and only reference branches that exist in the repository.