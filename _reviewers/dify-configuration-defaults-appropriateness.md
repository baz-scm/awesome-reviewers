---
title: Configuration defaults appropriateness
description: Ensure configuration parameters have appropriate default values and avoid
  hardcoded or overly specific settings. Default values should be conservative and
  safe for production environments, while avoiding personal assignments or environment-specific
  assumptions.
repository: langgenius/dify
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 114231
---

Ensure configuration parameters have appropriate default values and avoid hardcoded or overly specific settings. Default values should be conservative and safe for production environments, while avoiding personal assignments or environment-specific assumptions.

Examples of good practices:
- Use conservative defaults: `WORKFLOW_LOG_CLEANUP_ENABLED: ${WORKFLOW_LOG_CLEANUP_ENABLED:-false}` instead of `true`
- Provide sensible defaults for optional parameters like expiration times
- Remove inappropriate hardcoded assignments like single-user `assignees` in configuration files
- Avoid mixing deployment concerns by keeping third-party service configurations separate from main application config

This ensures configurations are maintainable, secure by default, and appropriate for team environments rather than individual setups.