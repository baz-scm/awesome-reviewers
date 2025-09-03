---
title: Standardize environment versions
description: Ensure consistent versions of languages, tools, and dependencies across
  all CI/CD environments (GitHub Actions, CircleCI, local development, etc.). Inconsistent
  versions between environments make it difficult to reproduce issues and debug failures,
  as seen when using "Python 3.12 in GitHub & 3.9 elsewhere - makes it hard to figure
  out how to fix the broken...
repository: BerriAI/litellm
label: CI/CD
language: Yaml
comments_count: 3
repository_stars: 28310
---

Ensure consistent versions of languages, tools, and dependencies across all CI/CD environments (GitHub Actions, CircleCI, local development, etc.). Inconsistent versions between environments make it difficult to reproduce issues and debug failures, as seen when using "Python 3.12 in GitHub & 3.9 elsewhere - makes it hard to figure out how to fix the broken unit tests."

Define a single source of truth for version specifications and reference it across all pipeline configurations. This includes:
- Runtime versions (Python, Node.js, etc.)
- Tool versions (Docker, kubectl, etc.) 
- Action/orb versions in CI systems

Example approach:
```yaml
# .tool-versions or similar
python 3.12.0
node 18.17.0
docker 24.0.0

# Reference in GitHub Actions
- uses: actions/setup-python@v4
  with:
    python-version: '3.12.0'

# Reference in CircleCI  
- image: cimg/python:3.12.0
```

This prevents environment drift, reduces debugging complexity, and ensures consistent behavior across all stages of your CI/CD pipeline.