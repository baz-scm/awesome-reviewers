---
title: Use descriptive names
description: Variable, method, and class names should clearly and accurately describe
  their purpose, content, or behavior. Misleading or vague names create confusion
  and make code harder to understand and maintain.
repository: python-poetry/poetry
label: Naming Conventions
language: Python
comments_count: 7
repository_stars: 33496
---

Variable, method, and class names should clearly and accurately describe their purpose, content, or behavior. Misleading or vague names create confusion and make code harder to understand and maintain.

Examples of improvements:
- Rename variables to match their actual content: `local_repo` → `lockfile_repo` when it specifically holds lockfile data
- Use action-based names for fixtures: `repo_with_packages` → `repo_add_default_packages` to reflect what it does
- Choose method names that reflect actual behavior: `get_system_python()` → `get_running_python()` when it returns the currently executing Python
- Name parameters clearly: `cached` → `cached_wheel` when specifically referring to wheel caching
- Avoid names that contradict functionality: a `module_name()` function should not do the opposite of converting module names

When reviewing code, ask: "Does this name accurately tell me what this thing is or does?" If there's any ambiguity or if the name could mislead someone reading the code, choose a more descriptive alternative.