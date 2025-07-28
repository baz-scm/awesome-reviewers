---
title: organize environment configurations
description: Environment variables in CI/CD workflows should be organized consistently
  using structured `env` sections rather than inline declarations, and should account
  for platform-specific requirements. This improves maintainability, readability,
  and prevents environment-related failures across different operating systems.
repository: cline/cline
label: Configurations
language: Yaml
comments_count: 2
repository_stars: 48299
---

Environment variables in CI/CD workflows should be organized consistently using structured `env` sections rather than inline declarations, and should account for platform-specific requirements. This improves maintainability, readability, and prevents environment-related failures across different operating systems.

Use the `env` field at the step or job level instead of inline variable assignments:

```yaml
# Preferred approach
- name: Package and Publish Extension
  env:
    VSCE_PAT: ${{ secrets.VSCE_PAT }}
    OVSX_PAT: ${{ secrets.OVSX_PAT }}
    CLINE_ENVIRONMENT: production
  run: vsce package --out "cline-${{ steps.get_version.outputs.version }}.vsix"

# Instead of inline
run: CURRENT_ENVIRONMENT=production vsce package --out "file.vsix"
```

For cross-platform compatibility, explicitly set platform-specific environment variables when needed:

```yaml
run: |
  # Default the encoding to UTF-8 - It's not the default on Windows
  PYTHONUTF8=1 PYTHONPATH=.github/scripts python -m coverage_check
```

This approach centralizes environment configuration, makes dependencies explicit, and prevents platform-specific failures in automated workflows.