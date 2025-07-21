---
title: Explicit CI configuration conditions
description: When writing CI/CD workflow configurations, always use explicit and precise
  conditions, paths, and selectors to ensure that actions only execute when necessary
  and operate on the exact intended targets. This prevents wasted compute resources,
  unintended side effects, and improves workflow reliability.
repository: temporalio/temporal
label: CI/CD
language: Yaml
comments_count: 2
repository_stars: 14953
---

When writing CI/CD workflow configurations, always use explicit and precise conditions, paths, and selectors to ensure that actions only execute when necessary and operate on the exact intended targets. This prevents wasted compute resources, unintended side effects, and improves workflow reliability.

For file paths in artifact uploads or processing steps, specify exact patterns instead of entire directories:
```yaml
# Instead of this (too broad):
path: .testoutput

# Use this (precise):
path: ./.testoutput/junit.*.xml
```

For conditional execution, include all necessary checks to ensure steps only run when appropriate:
```yaml
# Instead of this (missing check):
if: ${{ inputs.run_single_functional_test != true || (inputs.run_single_functional_test == true && contains(fromJSON(needs.set-up-single-test.outputs.dbs), env.PERSISTENCE_DRIVER)) }}

# Use this (complete check):
if: ${{ toJson(matrix.containers) != '[]' && (inputs.run_single_functional_test != true || (inputs.run_single_functional_test == true && contains(fromJSON(needs.set-up-single-test.outputs.dbs), env.PERSISTENCE_DRIVER))) }}
```

This practice reduces CI resource usage, prevents accidental inclusion of unwanted files in artifacts, and makes debugging workflow issues significantly easier.