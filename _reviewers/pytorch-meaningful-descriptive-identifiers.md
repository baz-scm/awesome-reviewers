---
title: Meaningful descriptive identifiers
description: Choose identifiers (variable/function/class names) that clearly convey
  their purpose and follow established conventions. Variable names should be semantically
  meaningful, accurately reflecting their content and usage throughout their lifecycle.
repository: pytorch/pytorch
label: Naming Conventions
language: Python
comments_count: 8
repository_stars: 91169
---

Choose identifiers (variable/function/class names) that clearly convey their purpose and follow established conventions. Variable names should be semantically meaningful, accurately reflecting their content and usage throughout their lifecycle.

Key guidelines:
- Use descriptive names over vague ones (e.g., `zip_path` instead of `new_path` when handling zip files)
- Avoid Python reserved keywords (e.g., use `input_` instead of `input`)
- Prefix internal/private functions with a single underscore (e.g., `_detect_linux_pkg_manager`)
- Avoid redundant prefixes in nested namespaces (e.g., no `cpp_` prefix for members already in a `cpp` class)
- Choose more descriptive method names that clearly express their purpose:
  ```python
  # Less clear:
  self.skip_mutation(var)
  self.remove_skip_mutation(var)
  
  # More clear:
  self.ignore_mutations_on(var)
  self.stop_ignoring_mutations_on(var)
  ```
- Prefer objective, technical terms over subjective descriptors (e.g., `topk` rather than `fast`)

When variable usage changes during implementation, rename accordingly to maintain semantic clarity.
