---
title: Standardize dependency management
description: Maintain consistent dependency management practices across CI workflows
  to ensure reliable builds and tests. Use the same tool (e.g., UV, PDM) throughout
  workflows and specify Python versions explicitly. Avoid redundant dependency specifications
  when dependencies are already included in other groups.
repository: pydantic/pydantic
label: CI/CD
language: Yaml
comments_count: 6
repository_stars: 24377
---

Maintain consistent dependency management practices across CI workflows to ensure reliable builds and tests. Use the same tool (e.g., UV, PDM) throughout workflows and specify Python versions explicitly. Avoid redundant dependency specifications when dependencies are already included in other groups.

Example:
```yaml
- uses: astral-sh/setup-uv@v5
  with:
    python-version: ${{ matrix.python-version }}
    enable-cache: true

- name: Install dependencies
  run: uv sync --python ${{ matrix.python-version }} --group testing --extra timezone
```

When installing dependencies, verify that you're not specifying extras that are already included in other groups. Keep tool configurations as close as possible to the upstream project's CI when working with third-party integrations.