---
title: Document configuration decisions
description: Configuration files should be self-explanatory and maintainable by including
  explicit version constraints and explanatory comments for non-obvious choices. This
  prevents future confusion and ensures reproducible environments.
repository: browser-use/browser-use
label: Configurations
language: Toml
comments_count: 2
repository_stars: 69139
---

Configuration files should be self-explanatory and maintainable by including explicit version constraints and explanatory comments for non-obvious choices. This prevents future confusion and ensures reproducible environments.

For dependencies, always specify version constraints rather than leaving them open-ended:
```toml
dependencies = [
    "anyio>=4.9.0",  # Not just "anyio"
]
```

For configuration choices that might seem unusual, add comments explaining the reasoning:
```toml
[tool.ruff.lint]
select = ["ASYNC", "E", "F", "I", "PLE"]
ignore = ["ASYNC109", "E101", "E402", "E501", "F841", "E731"]  # TODO: determine if adding timeouts to all the unbounded async functions is needed / worth-it so we can un-ignore ASYNC109
```

This practice helps future maintainers understand the rationale behind configuration decisions and makes it easier to revisit choices when requirements change.