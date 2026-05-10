---
title: Use semantic names
description: Use intention-revealing, consistent, and unique names for CI workflow,
  jobs, and steps (avoid generic labels like `build`). Names should tell the reader
  what the unit actually does.
repository: TheAlgorithms/Python
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 220912
---

Use intention-revealing, consistent, and unique names for CI workflow, jobs, and steps (avoid generic labels like `build`). Names should tell the reader what the unit actually does.

Apply:
- Workflow `name:`: describe the pipeline purpose (not “build”).
- Job `name:`: match the job’s responsibility; avoid multiple jobs called `build`.
- Step `name:`: explain the action; prefer specific labels that reflect the command/task.

Example (GitHub Actions):
```yaml
name: Build CI/CD Pipeline

jobs:
  build_and_test:
    name: Build and Test
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v5
      - name: Set up uv
        uses: astral-sh/setup-uv@v3
      - name: Install dependencies
        run: uv sync --group=test

  directory_writer:
    name: Directory Writer
    # ...
```
This improves readability and reduces confusion when multiple workflows/jobs/steps exist.