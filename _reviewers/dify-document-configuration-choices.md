---
title: Document configuration choices
description: Configuration scripts and files should clearly document non-obvious choices,
  especially numeric IDs, special values, and environment-specific commands. Include
  comments explaining the purpose and reasoning behind configuration decisions to
  help future maintainers understand why specific values or approaches were chosen.
repository: langgenius/dify
label: Configurations
language: Shell
comments_count: 2
repository_stars: 114231
---

Configuration scripts and files should clearly document non-obvious choices, especially numeric IDs, special values, and environment-specific commands. Include comments explaining the purpose and reasoning behind configuration decisions to help future maintainers understand why specific values or approaches were chosen.

When using numeric user/group IDs, always document which user they represent:

```bash
# Set ownership to proxy user (UID 13) required for Squid operation
chown -R 13:13 /var/log/squid
```

Additionally, verify that configuration commands work reliably across environments. Avoid commands with known compatibility issues and prefer more explicit alternatives:

```bash
# Use explicit directory change instead of -C flag due to poetry issue #9415
cd api && poetry install
```

This practice prevents configuration failures and reduces debugging time when scripts don't work as expected in different environments.