---
title: Scope and document configurations
description: 'When designing and implementing configuration options, carefully consider
  two key aspects:


  1. **Choose appropriate configuration scope**: Place configuration settings at the
  level that makes the most sense for their purpose and usage pattern. Avoid overly
  granular scopes when settings could logically apply at a broader level.'
repository: elastic/elasticsearch
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 73104
---

When designing and implementing configuration options, carefully consider two key aspects:

1. **Choose appropriate configuration scope**: Place configuration settings at the level that makes the most sense for their purpose and usage pattern. Avoid overly granular scopes when settings could logically apply at a broader level.

   ```
   // Prefer index-level settings for behaviors that affect the entire index
   // Example from Discussion 1:
   "early_termination": true   // At index level, not field level
   ```

2. **Document configurations completely**: Provide clear documentation that covers all possible values, edge cases, and boundary conditions. Explicitly state limitations, especially for managed environments where configuration options may be restricted.

   ```
   // Example of improved documentation clarity:
   // Before:
   "50% of total system memory when more than 1 GB, with a maximum of 31 GB."
   
   // After:
   "50% of total system memory when 1 GB or more, with a maximum of 31 GB."
   ```

For managed or restricted environments, clearly explain which configuration options are available to users and why certain configurations might be limited or handled automatically.
