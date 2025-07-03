---
title: Optimize container build configurations
description: Configure containerized application builds to be efficient and flexible
  by avoiding hardcoded architecture decisions and using appropriate compiler flags.
  Let the build system determine architecture targeting instead of maintaining architecture-specific
  code blocks in your Dockerfiles. For Go applications, use appropriate build flags
  like `CGO_ENABLED=0` to...
repository: kubeflow/kubeflow
label: CI/CD
language: Dockerfile
comments_count: 2
repository_stars: 15064
---

Configure containerized application builds to be efficient and flexible by avoiding hardcoded architecture decisions and using appropriate compiler flags. Let the build system determine architecture targeting instead of maintaining architecture-specific code blocks in your Dockerfiles. For Go applications, use appropriate build flags like `CGO_ENABLED=0` to enable static linking and optimize container images.

**Example:**
Instead of:
```dockerfile
RUN if [ "$(uname -m)" = "aarch64" ]; then \
        CGO_ENABLED=0 GOOS=linux GOARCH=arm64 go build -o webhook -a . ; \
    else \
        CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o webhook -a . ; \
    fi
```

Prefer:
```dockerfile
RUN CGO_ENABLED=0 GOOS=linux go build -o webhook -ldflags "-w" -a .
```

This approach simplifies maintenance, allows multi-architecture builds through tools like Docker buildx (e.g., `docker buildx build --platform linux/amd64,linux/arm64 ...`), and produces more efficient container images.
