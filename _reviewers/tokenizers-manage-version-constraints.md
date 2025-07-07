---
title: Manage version constraints
description: 'When configuring dependency version constraints in project files, follow
  these principles:


  1. Be explicit about version ranges to balance flexibility with stability:'
repository: huggingface/tokenizers
label: Configurations
language: Toml
comments_count: 3
repository_stars: 9868
---

When configuring dependency version constraints in project files, follow these principles:

1. Be explicit about version ranges to balance flexibility with stability:
   - Allow minor version updates while preventing breaking changes
   - Example: `dependencies = ["huggingface_hub>=0.16.4,<1.0"]` instead of `<0.17`

2. Update interdependent packages together:
   - For packages that must be synchronized (like PyO3 and numpy), update them in tandem
   - Example: 
     ```toml
     pyo3 = "0.16.2"
     numpy = "0.16.2"
     ```

3. Separate dependency updates in version control:
   - Submit dependency updates in dedicated PRs rather than bundling them with other changes
   - This makes review and validation simpler, especially for detecting potential breaking changes