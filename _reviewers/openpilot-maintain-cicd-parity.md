---
title: maintain CI/CD parity
description: Ensure CI/CD pipeline tools run with the same configuration, flags, and
  behavior as developers use locally. This prevents masking errors in CI/CD that developers
  would encounter in their local environment and maintains consistency in the development
  workflow.
repository: commaai/openpilot
label: CI/CD
language: Shell
comments_count: 2
repository_stars: 58214
---

Ensure CI/CD pipeline tools run with the same configuration, flags, and behavior as developers use locally. This prevents masking errors in CI/CD that developers would encounter in their local environment and maintains consistency in the development workflow.

When configuring linting, testing, or other quality tools in CI/CD scripts, avoid adding flags or modifications that change the tool's behavior compared to local usage. For example, avoid adding `--quiet` flags or different file selection criteria that could hide issues developers need to see.

Example of what to avoid:
```bash
# This masks errors that developers see locally
run "ruff" ruff check $PYTHON_FILES --quiet
```

Instead, ensure CI/CD runs the same commands developers would run:
```bash
# This matches what developers run locally: "ruff check ."
run "ruff" ruff check $PYTHON_FILES
```

This principle applies to all CI/CD tools including linters, formatters, test runners, and build tools. The goal is to eliminate surprises where something passes in CI/CD but fails locally, or vice versa.