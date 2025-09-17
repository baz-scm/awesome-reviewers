---
title: Conservative configuration management
description: Be selective and intentional with configuration choices to avoid bloat
  and unnecessary complexity. This applies to build configurations, development environment
  settings, and dependency management.
repository: langgenius/dify
label: Configurations
language: Json
comments_count: 3
repository_stars: 114231
---

Be selective and intentional with configuration choices to avoid bloat and unnecessary complexity. This applies to build configurations, development environment settings, and dependency management.

Key practices:
- Exclude unnecessary directories and files from build processes to improve performance
- Make optional development features configurable rather than enabled by default
- Avoid introducing new dependencies unless existing solutions cannot fulfill requirements
- Document optional configurations clearly so developers can enable them when needed

Example from TypeScript configuration:
```json
"exclude": [
  "**/node_modules/**",
  "**/.next/**"
]
```

This approach reduces build times, keeps development environments lean, and minimizes maintenance overhead while ensuring configurations remain focused on actual project needs.