---
title: Decouple CI from code
description: Separate CI configuration from code that serves other purposes. When
  variables or settings affect both user-facing behavior and CI pipeline behavior,
  extract CI-specific logic into dedicated configuration files. This prevents unintended
  CI pipeline changes when updating user-facing functionality and allows for better
  coordination between code changes and CI...
repository: Homebrew/brew
label: CI/CD
language: Shell
comments_count: 2
repository_stars: 44168
---

Separate CI configuration from code that serves other purposes. When variables or settings affect both user-facing behavior and CI pipeline behavior, extract CI-specific logic into dedicated configuration files. This prevents unintended CI pipeline changes when updating user-facing functionality and allows for better coordination between code changes and CI environment updates.

For example, instead of:
```bash
# This controls both user warnings and CI runners
HOMEBREW_MACOS_OLDEST_SUPPORTED="13"
```

Refactor to:
```bash
# User-facing support declaration
HOMEBREW_MACOS_OLDEST_SUPPORTED="13"

# CI configuration in a separate file (github_runner_matrix.rb)
HOMEBREW_CI_MACOS_VERSIONS = ["13", "14"]
```

This separation allows you to control the timing of CI environment changes independently from feature changes, ensuring proper sequencing of: code changes, release tagging, and then CI environment updates.