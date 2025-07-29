---
title: consistent semantic naming
description: Names should follow established team conventions while accurately reflecting
  their purpose and functionality. Inconsistent naming schemes and misleading identifiers
  create confusion and maintenance overhead.
repository: python-poetry/poetry
label: Naming Conventions
language: Yaml
comments_count: 2
repository_stars: 33496
---

Names should follow established team conventions while accurately reflecting their purpose and functionality. Inconsistent naming schemes and misleading identifiers create confusion and maintenance overhead.

When naming identifiers, ensure they:
1. Adhere to established team naming patterns (e.g., use slashes instead of spaces in labels)
2. Accurately describe what the identifier represents or does

Examples:
- Instead of `test poetry export` (violates naming scheme), use `test/export`
- Instead of `poetry-update` (misleading - doesn't actually update), use `poetry-sync` (accurately reflects synchronization behavior)

This applies to all identifiers including variables, functions, classes, configuration keys, labels, and hook names. Consistent and accurate naming improves code readability and reduces cognitive load for team members.