---
title: Use descriptive parameter names
description: Parameter names should clearly indicate their purpose and avoid ambiguity
  or conflicts with existing constructs in the codebase context. Names should be self-explanatory
  without requiring additional comments or context to understand their function.
repository: snyk/cli
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 5178
---

Parameter names should clearly indicate their purpose and avoid ambiguity or conflicts with existing constructs in the codebase context. Names should be self-explanatory without requiring additional comments or context to understand their function.

When naming parameters, consider:
- Whether the name conflicts with existing constructs or has special meaning in the current context
- Whether the name clearly communicates what the parameter represents or is used for
- Whether someone unfamiliar with the code would understand the parameter's purpose

Example of problematic naming:
```yaml
# Confusing - "executor" has special meaning in CircleCI
- install-deps-python:
    executor: win-something

# Unclear purpose
go_base_url: 'https://go.dev/dl/'
```

Example of improved naming:
```yaml
# Clear and doesn't conflict with CircleCI constructs  
- install-deps-python:
    os: win-something

# Descriptive and obvious purpose
go_download_base_url: 'https://go.dev/dl/'
```

This practice reduces cognitive load for developers and prevents misunderstandings about parameter usage.