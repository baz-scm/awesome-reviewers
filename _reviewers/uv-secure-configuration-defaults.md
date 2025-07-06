---
title: Secure configuration defaults
description: Establish secure default configurations in project metadata files to
  prevent accidental publishing and ensure proper version constraints. This is particularly
  important for private packages and build system configurations.
repository: astral-sh/uv
label: Configurations
language: Markdown
comments_count: 5
repository_stars: 60322
---

Establish secure default configurations in project metadata files to prevent accidental publishing and ensure proper version constraints. This is particularly important for private packages and build system configurations.

Key practices:
1. Add the "Private :: Do Not Upload" classifier for non-public packages:
```toml
[project]
classifiers = [
    "Private :: Do Not Upload",
    # Other classifiers...
]
```

2. Use appropriate version constraints in build system requirements:
```toml
[build-system]
# Prefer narrow version ranges for build backends
requires = ["uv>=0.4.18,<0.5"]
```

3. Validate completeness of required configuration fields:
- Ensure project.name is specified
- Include explicit version information
- Define clear build system requirements

This approach helps prevent accidental package uploads to public repositories and ensures reproducible builds through proper version constraints.