---
title: specify configuration scope
description: Always explicitly specify the configuration scope using `--user` or `--repo`
  flags when setting configuration values with `jj config set`. This prevents ambiguity
  about where the configuration should be stored and ensures settings are applied
  at the intended level.
repository: jj-vcs/jj
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 21171
---

Always explicitly specify the configuration scope using `--user` or `--repo` flags when setting configuration values with `jj config set`. This prevents ambiguity about where the configuration should be stored and ensures settings are applied at the intended level.

Use `--user` for settings that should apply across all repositories for the current user, and `--repo` for settings specific to the current repository.

Example:
```shell
# Repository-specific configuration
jj config set --repo 'revset-aliases."trunk()"' main@upstream
jj config set --repo gerrit.default_for main

# User-wide configuration  
jj config set --user gerrit.default_for main
jj config set --user git.push origin
```

Without explicit scope specification, it's unclear whether the configuration will be stored in the user's global config or the repository's local config, leading to unexpected behavior and configuration management issues.