---
title: specify tool version requirements
description: When documenting CI/CD tools and integrations, always specify exact version
  requirements and compatibility constraints. This prevents integration failures and
  ensures reproducible builds across different environments.
repository: python-poetry/poetry
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 33496
---

When documenting CI/CD tools and integrations, always specify exact version requirements and compatibility constraints. This prevents integration failures and ensures reproducible builds across different environments.

Include specific version numbers using comparison operators (>=, >, ==) rather than vague statements like "recent versions" or "supported versions". When possible, provide fallback instructions or alternative configurations for older versions that teams might still be using.

Example:
```markdown
**Yes**. Provided that you are using `tox` >= 4, you can use it in combination with
the PEP 517 compliant build system provided by Poetry. (With tox 3, you have to set the 
[isolated build](https://tox.wiki/en/3.27.1/config.html#conf-isolated_build) option.)
```

This approach helps teams understand exactly what they need to install or upgrade, and provides clear migration paths when updating their CI/CD pipelines.