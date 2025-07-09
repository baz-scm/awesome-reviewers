---
title: Use descriptive identifiers
description: Choose clear, meaningful names for variables, parameters, and constants
  that convey their purpose without requiring additional documentation or context.
repository: neondatabase/neon
label: Naming Conventions
language: Python
comments_count: 5
repository_stars: 19015
---

Choose clear, meaningful names for variables, parameters, and constants that convey their purpose without requiring additional documentation or context.

Key practices:
1. **Use semantic names instead of indices**: Replace cryptic array indices with descriptive variable names.
   ```python
   # Instead of this:
   assert prewarm_info[0] > 0 and prewarm_info[1] > 0
   
   # Do this:
   total, prewarmed, skipped = prewarm_info
   assert total > 0 and prewarmed > 0
   ```

2. **Apply consistent prefixes** for related parameters to indicate their domain:
   ```python
   # Instead of this:
   disable_kick_secondary_downloads: bool = False
   
   # Do this:
   storcon_kick_secondary_downloads: bool = True
   ```

3. **Use standard naming conventions** like uppercase for constants:
   ```python
   # Instead of this:
   prewarm_label = "compute_ctl_lfc_prewarm_requests_total"
   
   # Do this:
   PREWARM_LABEL = "compute_ctl_lfc_prewarm_requests_total"
   ```

4. **Avoid negatively named booleans** and consider enums for complex options:
   ```python
   # Instead of this:
   def test_lfc_prewarm(neon_simple_env: NeonEnv, with_compute_ctl: bool):
       """with_compute_ctl: Test compute ctl's methods instead of querying Postgres directly"""
   
   # Do this:
   class LfcQueryMethod(Enum):
       COMPUTE_CTL = "compute_ctl"
       POSTGRES = "postgres"
       
   def test_lfc_prewarm(neon_simple_env: NeonEnv, query: LfcQueryMethod):
   ```

Clear naming reduces cognitive load, minimizes the need for comments, and makes code more maintainable and easier to understand at first glance.