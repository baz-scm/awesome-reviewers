---
title: Consistent naming conventions
description: 'Maintain consistent naming patterns throughout the codebase to improve
  readability and reduce confusion:


  1. **Use descriptive names that reflect purpose**:'
repository: bridgecrewio/checkov
label: Naming Conventions
language: Python
comments_count: 10
repository_stars: 7668
---

Maintain consistent naming patterns throughout the codebase to improve readability and reduce confusion:

1. **Use descriptive names that reflect purpose**:
   - Boolean functions should use prefixes like `is_`, `has_`, or `should_` (e.g., `_should_prioritise_secrets` instead of `_prioritise_secrets`)
   - Loop variables should be descriptive (e.g., `resource` or `changed_resource` instead of `each`)
   - Classes should have specific names that avoid ambiguity (e.g., `TerraformJsonRunner` instead of `Runner`)

2. **Follow project style conventions**:
   - Use snake_case for variables and functions (e.g., `self.data_flow` not `self.dataflow`)
   - Use underscores in file names instead of spaces (e.g., `a_example_skip` not `a example skip`)
   - Prefix environment variables with `CHECKOV_` for internal vars
   - Use distinctive names for utility functions to avoid IDE confusion (e.g., `pickle_deepcopy` instead of just `deepcopy`)

3. **Use consistent type hint syntax**:
   - Prefer modern Union syntax: `str | None` instead of `Optional[str]`
   - Use lowercase type aliases: `tuple` instead of `Tuple`

These conventions make code easier to understand, maintain, and debug while reducing the cognitive load for developers working across different parts of the codebase.