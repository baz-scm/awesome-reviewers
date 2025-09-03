---
title: optimize Docker layers
description: Avoid unnecessary duplication and bloat in Docker layers by trusting
  base images to provide standard tools and using appropriate installation methods.
  Instead of upgrading pip when the base image already provides it, trust the image's
  version to prevent duplicate copies across layers. When installing application code,
  use editable installs to avoid creating...
repository: browser-use/browser-use
label: Configurations
language: Dockerfile
comments_count: 3
repository_stars: 69139
---

Avoid unnecessary duplication and bloat in Docker layers by trusting base images to provide standard tools and using appropriate installation methods. Instead of upgrading pip when the base image already provides it, trust the image's version to prevent duplicate copies across layers. When installing application code, use editable installs to avoid creating duplicate copies of the codebase in different layers.

Example of problematic approach:
```dockerfile
RUN pip install --upgrade pip \
    && pip install .
```

Preferred approach:
```dockerfile
# Trust base image pip version, use editable install
RUN pip install -e .
```

This reduces image size, build time, and layer complexity while maintaining the same functionality. Apply this principle to other tools and dependencies - only install what's not already provided by the base image.