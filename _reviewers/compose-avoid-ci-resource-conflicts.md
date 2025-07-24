---
title: avoid CI resource conflicts
description: Design CI workflows to prevent resource conflicts when multiple builds
  run concurrently on shared infrastructure. This includes using unique identifiers
  for temporary resources, minimizing container privileges, and separating CI-specific
  operations from local development workflows.
repository: docker/compose
label: CI/CD
language: Other
comments_count: 3
repository_stars: 35858
---

Design CI workflows to prevent resource conflicts when multiple builds run concurrently on shared infrastructure. This includes using unique identifiers for temporary resources, minimizing container privileges, and separating CI-specific operations from local development workflows.

Key practices:
- Use unique container names with timestamps or build IDs to prevent naming conflicts
- Avoid hardcoded paths or names that could clash between parallel builds  
- Minimize container privileges (avoid --privileged unless absolutely necessary)
- Keep CI-specific setup steps in CI configuration files rather than in Makefiles used for local development

Example of problematic code:
```bash
TMP_CONTAINER="tmpcontainer"  # Fixed name causes conflicts
docker run --privileged ...   # Unnecessary privileges
```

Better approach:
```bash
TMP_CONTAINER="tmpcontainer-$(date +%s)-$$"  # Unique per run
docker run ...  # Only add --privileged if actually needed
```

This prevents build failures when multiple PRs or builds execute simultaneously on shared CI infrastructure, and ensures local development workflows remain usable without requiring system-level permissions.