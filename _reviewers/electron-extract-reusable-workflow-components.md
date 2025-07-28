---
title: extract reusable workflow components
description: Avoid duplicating workflow steps across multiple CI/CD pipelines by extracting
  common functionality into reusable actions. This improves maintainability, reduces
  inconsistencies, and ensures proper cross-platform compatibility when needed.
repository: electron/electron
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 117644
---

Avoid duplicating workflow steps across multiple CI/CD pipelines by extracting common functionality into reusable actions. This improves maintainability, reduces inconsistencies, and ensures proper cross-platform compatibility when needed.

When you find yourself copying similar workflow steps across multiple pipeline files, create a composite action instead. Pay special attention to cross-platform scenarios where caching or other features may require specific configuration.

Example of extracting a common dependency installation step:

```yaml
# Before: Duplicated across multiple workflows
- name: Get yarn cache directory path
  # ... repeated setup code

# After: Extract to .github/actions/install-dependencies/action.yml
- name: Install Dependencies
  uses: ./.github/actions/install-dependencies
  with:
    enable-cross-platform-cache: true
```

For cross-platform workflows, ensure proper configuration like `enableCrossOsArchive: true` when caching between different operating systems. This prevents cache restoration failures when artifacts are saved on one platform and restored on another.