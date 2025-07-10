---
title: Document containerized builds
description: When using Docker for build environments, provide complete, tested instructions
  that users can copy-paste without modification. Include proper user permission handling
  to prevent file ownership issues, and ensure commands work as documented.
repository: maplibre/maplibre-native
label: CI/CD
language: Markdown
comments_count: 2
repository_stars: 1411
---

When using Docker for build environments, provide complete, tested instructions that users can copy-paste without modification. Include proper user permission handling to prevent file ownership issues, and ensure commands work as documented.

For example, instead of generic placeholders:
```bash
# DON'T
docker run --rm -it -v "$PWD:/code/" -u $(id -u):$(id -g) maplibre-native-image ___any_build_command___
```

Provide specific working examples:
```bash
# DO
docker build \
  -t maplibre-native-image \
  --build-arg USER_ID=$(id -u) \
  --build-arg GROUP_ID=$(id -g) \
  -f platform/linux/Dockerfile \
  platform/linux

# Run all build commands using the docker container
docker run --rm -it -v "$PWD:/code/" maplibre-native-image
```

This ensures reproducible builds across different developer environments and CI/CD pipelines, reduces setup time, and prevents "works on my machine" issues.