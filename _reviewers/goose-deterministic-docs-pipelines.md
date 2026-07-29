---
title: Deterministic Docs Pipelines
description: "For CI/CD that builds/publishes documentation (or any release-time artifacts),\
  \ ensure two things: \n1) **Correct trigger coverage**: docs-only changes must run\
  \ the docs build via an explicit workflow path (don’t assume upstream jobs will\
  \ run). If you use `paths-ignore` to skip heavy pipelines on doc changes, add a\
  \ separate workflow (or separate trigger) that..."
repository: aaif-goose/goose
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 51876
---

For CI/CD that builds/publishes documentation (or any release-time artifacts), ensure two things: 
1) **Correct trigger coverage**: docs-only changes must run the docs build via an explicit workflow path (don’t assume upstream jobs will run). If you use `paths-ignore` to skip heavy pipelines on doc changes, add a separate workflow (or separate trigger) that fires on `documentation/**` so docs always get published.
2) **Reproducible source fetching**: when the workflow or docs install script clones external repos, pin to an immutable commit SHA (not a moving tag) so outputs can’t change unexpectedly.

Example (workflow trigger separation):
```yaml
# docs-bundle.yml
on:
  workflow_call:
    inputs:
      force_build: { type: boolean }
  push:
    branches: [main, "release/*"]
    paths:
      - "documentation/**"
  workflow_dispatch:
```

Example (immutable pin in an installer script):
```bash
HERDR_SETUP=$(mktemp -d) && \
git clone https://github.com/modib/agent-toolkit.git "$HERDR_SETUP" && \
cd "$HERDR_SETUP" && \
git checkout bfe921c7608861c58ea37aac981b32eb3032915e
```