---
title: Avoid hardcoded configuration values
description: Configuration files and scripts should use placeholders, environment
  variables, or parameterized values instead of hardcoding specific configuration
  values. Hardcoded values make configurations inflexible and difficult to adapt across
  different environments or deployments.
repository: LMCache/LMCache
label: Configurations
language: Shell
comments_count: 2
repository_stars: 3800
---

Configuration files and scripts should use placeholders, environment variables, or parameterized values instead of hardcoding specific configuration values. Hardcoded values make configurations inflexible and difficult to adapt across different environments or deployments.

Use placeholder formats that clearly indicate what type of value should be provided:

```bash
# Good - uses placeholder format
IMAGE=<IMAGE_NAME>:<TAG>

# Avoid - hardcoded specific values
IMAGE=lmcache/vllm-openai:2025-05-17-v1
```

This approach ensures configurations remain flexible and can be easily customized for different environments, deployments, or use cases without requiring code changes.