---
title: Environment variable consistency
description: Ensure consistent formatting and proper usage of environment variables
  in Dockerfiles. Remove unnecessary quotes from ENV declarations and choose between
  ARG and ENV based on their intended scope - use ARG for build-time configuration
  that may change between builds, and ENV for runtime configuration that containers
  need during execution.
repository: comfyanonymous/ComfyUI
label: Configurations
language: Dockerfile
comments_count: 3
repository_stars: 83726
---

Ensure consistent formatting and proper usage of environment variables in Dockerfiles. Remove unnecessary quotes from ENV declarations and choose between ARG and ENV based on their intended scope - use ARG for build-time configuration that may change between builds, and ENV for runtime configuration that containers need during execution.

Key guidelines:
- Remove unnecessary quotes from ENV values unless the value contains spaces or special characters
- Use ARG for build-time parameters that configure the build process
- Use ENV when the variable needs to be available during container runtime or in RUN commands
- Maintain consistency in formatting across all environment variable declarations

Example:
```dockerfile
# Good - consistent formatting, appropriate usage
ARG PYTHON_VERSION=3.11
ENV PIP_CACHE_DIR=/cache/pip
ENV VIRTUAL_ENV=/app/venv
ENV TRANSFORMERS_CACHE=/app/.cache/transformers

# Avoid - unnecessary quotes and inconsistent formatting  
ENV PIP_CACHE_DIR="/cache/pip"
ENV VIRTUAL_ENV=/app/venv
ENV TRANSFORMERS_CACHE="/app/.cache/transformers"
```

This approach improves readability, reduces confusion about when quotes are necessary, and ensures proper separation between build-time and runtime configuration.