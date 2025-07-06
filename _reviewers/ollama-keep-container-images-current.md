---
title: Keep container images current
description: 'Always use up-to-date and supported container images in Dockerfiles
  and configuration files. Before specifying a base image or version:


  1. Verify the image hasn''t been deprecated'
repository: ollama/ollama
label: Configurations
language: Dockerfile
comments_count: 2
repository_stars: 145705
---

Always use up-to-date and supported container images in Dockerfiles and configuration files. Before specifying a base image or version:

1. Verify the image hasn't been deprecated
2. Confirm the specified version is available in repositories
3. Consider cross-platform compatibility requirements

For example, instead of:
```dockerfile
FROM cosdt/cann:${ASCEND_VERSION} AS ascend-build-arm64
```

Use the recommended current alternative:
```dockerfile
FROM ascendai/cann:${ASCEND_VERSION} AS ascend-build-arm64
```

Similarly, when updating dependency versions like ROCm, verify availability and compatibility with your base OS image:
```dockerfile
# Check if this version exists with your base image before specifying
ARG ROCM_VERSION=6.3.2
```

When the desired version isn't available with your current base image, consider updating the base image itself (e.g., moving from centos-7 to almalinux-8 for newer ROCm versions).