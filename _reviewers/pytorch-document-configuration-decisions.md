---
title: Document configuration decisions
description: 'Always document configuration decisions in package metadata files like
  `pyproject.toml` with clear comments, especially when:


  1. Using deprecated formats due to technical constraints'
repository: pytorch/pytorch
label: Configurations
language: Toml
comments_count: 3
repository_stars: 91345
---

Always document configuration decisions in package metadata files like `pyproject.toml` with clear comments, especially when:

1. Using deprecated formats due to technical constraints
2. Setting version constraints that may affect compatibility
3. Making decisions that might need revisiting in the future

When configuration decisions deviate from best practices, include the reasoning and any relevant links or references. Additionally, implement linters to ensure consistency between related configuration sections (e.g., Python version constraints and classifiers).

Example:
```toml
[project]
# TODO: change to `license = "BSD-3-Clause"` and enable PEP 639 after pinning setuptools>=77
# FIXME: As of 2025.06.20, it is hard to ensure the minimum version of setuptools in our CI environment.
# TOML-table-based license deprecated in setuptools>=77, and the deprecation warning will be changed
# to an error on 2026.02.18. See also: https://github.com/pypa/setuptools/issues/4903
license = { text = "BSD-3-Clause" }

requires-python = ">=3.9"  # also update classifiers when changing this
```

This approach ensures that future developers understand the context behind configuration choices and helps maintain consistency across the codebase. It also creates clear reminders for revisiting temporary workarounds as technical constraints evolve.