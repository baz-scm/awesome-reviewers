---
title: Avoid hardcoded configuration values
description: Configuration values should be parameterized rather than hardcoded in
  scripts and tools. Hardcoded values make code less reusable and require manual updates
  when used in different contexts or projects.
repository: docker/compose
label: Configurations
language: Shell
comments_count: 2
repository_stars: 35858
---

Configuration values should be parameterized rather than hardcoded in scripts and tools. Hardcoded values make code less reusable and require manual updates when used in different contexts or projects.

Instead of embedding project-specific strings directly in code, use variables, parameters, or configuration files. This applies to project names, paths, environment variables, and other context-specific values.

Example of problematic hardcoded configuration:
```bash
if [[ "${k}" == "github.com/containerd/containerd"* ]]; then
    continue
fi
```

Better approach - parameterize the value:
```bash
if [[ "${k}" == "github.com/docker/compose"* ]]; then
    continue
fi
```

For environment variables and tool wrappers, ensure consistent behavior across different execution contexts. When wrapping tools, maintain the same environment variable handling as the original tool while avoiding hardcoded assumptions about paths or configurations.

This practice improves code reusability, reduces maintenance overhead, and prevents configuration-related bugs when code is used in different environments or projects.