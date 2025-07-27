---
title: synchronize configuration values
description: Ensure configuration values remain consistent and aligned across all
  related files, environments, and systems. When updating versions, parameters, or
  settings in one location, verify and update corresponding values in other configuration
  files to prevent mismatches that can lead to build failures or environment pollution.
repository: snyk/cli
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 5178
---

Ensure configuration values remain consistent and aligned across all related files, environments, and systems. When updating versions, parameters, or settings in one location, verify and update corresponding values in other configuration files to prevent mismatches that can lead to build failures or environment pollution.

Key practices:
- Keep version numbers synchronized between CircleCI configs, Dockerfiles, and package files
- Use environment-specific configurations (e.g., separate API keys for testing vs production) to prevent cross-contamination
- When updating dependency versions, ensure all related configuration files reflect the same versions
- Document the relationships between configuration files to make synchronization requirements clear

Example from CircleCI config:
```yaml
# Instead of hardcoding versions that may drift apart
executors:
  circle-go:
    docker:
      - image: cimg/go:1.20  # This should match Dockerfile version

# Consider using parameters for consistency
parameters:
  go_version:
    type: string
    default: "1.20"
```

This prevents issues where different parts of the system use incompatible versions or where test configurations accidentally affect production environments.