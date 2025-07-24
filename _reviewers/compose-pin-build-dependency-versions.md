---
title: Pin build dependency versions
description: Always pin specific versions for build dependencies and tools to prevent
  unexpected build failures, even when the dependency won't be shipped in the final
  product. While rolling tags may be convenient, explicit version pinning provides
  build reproducibility and prevents surprises from automatic updates.
repository: docker/compose
label: Configurations
language: Dockerfile
comments_count: 3
repository_stars: 35858
---

Always pin specific versions for build dependencies and tools to prevent unexpected build failures, even when the dependency won't be shipped in the final product. While rolling tags may be convenient, explicit version pinning provides build reproducibility and prevents surprises from automatic updates.

For build tools that don't ship with the final product, pin to specific versions to avoid sudden build breaks:

```dockerfile
# Pin specific versions for build stability
ARG GO_VERSION=1.21.0
ARG PYTHON_VERSION=3.7.9
# FIXME: virtualenv 16.3.0 breaks build, force 16.2.0 until fixed
RUN pip install virtualenv==16.2.0 tox==2.1.1
```

This approach is especially important for build tools and dependencies that are used during the build process but not included in the final image. Even if patch releases are generally safe, pinning versions ensures consistent builds across different environments and prevents unexpected failures when dependencies are automatically updated.