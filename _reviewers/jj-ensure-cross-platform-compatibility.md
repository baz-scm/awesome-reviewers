---
title: ensure cross-platform compatibility
description: When creating configuration files and build tasks, prioritize cross-platform
  compatibility by avoiding shell-specific syntax and considering how tools discover
  their configuration files across different environments.
repository: jj-vcs/jj
label: Configurations
language: Toml
comments_count: 2
repository_stars: 21171
---

When creating configuration files and build tasks, prioritize cross-platform compatibility by avoiding shell-specific syntax and considering how tools discover their configuration files across different environments.

Key considerations:
- Avoid shell-specific commands that may not work on Windows (e.g., complex piping with xargs)
- Consider how tools locate configuration files - some tools search parent directories automatically while others require explicit paths
- Test configuration discovery from different working directories, not just the project root
- Document platform limitations when unavoidable

Example from mise configuration:
```toml
[tasks."check:codespell"]
description = "Check code for common misspellings"
tools.uv = "{{vars.uv_version}}"
# Good: Uses tool that auto-discovers config, works cross-platform
run = "uv run codespell"

# Avoid: Shell-specific syntax that breaks on Windows
# run = "jj file list | xargs mise run codespell"
```

This approach ensures your development environment works consistently for all team members regardless of their operating system, reducing setup friction and debugging time spent on platform-specific issues.