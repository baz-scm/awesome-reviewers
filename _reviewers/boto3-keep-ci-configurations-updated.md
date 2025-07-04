---
title: Keep CI configurations updated
description: Regularly review and update CI configuration files to remove obsolete
  settings and use appropriate version specifications based on current platform capabilities.
  This minimizes configuration overhead, reduces maintenance burden, and ensures your
  CI pipeline remains efficient.
repository: boto/boto3
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 9417
---

Regularly review and update CI configuration files to remove obsolete settings and use appropriate version specifications based on current platform capabilities. This minimizes configuration overhead, reduces maintenance burden, and ensures your CI pipeline remains efficient.

For example, in Travis CI:
- Remove unnecessary `dist` and `sudo` settings that are no longer required
- Use stable version identifiers (e.g., "3.6" instead of "3.6-dev") unless specifically testing development versions
- Verify platform documentation is current by testing configurations directly when in doubt

```yaml
# Good: Clean configuration
python:
  - "3.5"
  - "3.6"
  - "3.7"
  - "3.8"

# Avoid: Unnecessary settings
python:
  - "3.5"
  - "3.6"
  - "3.7"
matrix:
  include:
    - python: 3.8
      dist: xenial   # Unnecessary if no longer required
      sudo: true     # Unnecessary if no longer required
```