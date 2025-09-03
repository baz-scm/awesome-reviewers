---
title: maintain clean linter configs
description: Ensure linter configuration files are well-maintained by avoiding duplicate
  entries, using current non-deprecated options, and implementing security-conscious
  restrictions. Remove any duplicate configuration blocks, replace deprecated linters
  with their modern equivalents, and configure restrictive policies for dangerous
  imports that require explicit...
repository: gofiber/fiber
label: Configurations
language: Yaml
comments_count: 3
repository_stars: 37560
---

Ensure linter configuration files are well-maintained by avoiding duplicate entries, using current non-deprecated options, and implementing security-conscious restrictions. Remove any duplicate configuration blocks, replace deprecated linters with their modern equivalents, and configure restrictive policies for dangerous imports that require explicit justification.

Example of good practices:
```yaml
# Remove duplicates - avoid this:
- name: unhandled-error
  arguments: ['bytes\.Buffer\.Write']
- name: unhandled-error  # Duplicate!
  disabled: true

# Use current linters - replace deprecated ones:
# - varcheck  # Deprecated
- unused      # Current alternative

# Configure security restrictions:
depguard:
  packages:
    - unsafe  # Require //nolint:depguard // Justification
```

This ensures configuration files remain clean, current, and secure while preventing maintenance issues and security oversights.