---
title: Configuration structure clarity
description: Ensure configuration parameters are properly structured, accurately documented,
  and clearly indicate their scope and purpose. Configuration hierarchies should be
  explicit (global, assistant-level, thread-level), parameter categories should be
  well-defined (init vs runtime), and documented values must match actual system behavior.
repository: menloresearch/jan
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 37620
---

Ensure configuration parameters are properly structured, accurately documented, and clearly indicate their scope and purpose. Configuration hierarchies should be explicit (global, assistant-level, thread-level), parameter categories should be well-defined (init vs runtime), and documented values must match actual system behavior.

Key practices:
- Categorize parameters by their lifecycle and mutability (e.g., `init` for initialization-time settings, `runtime` for dynamic updates)
- Document configuration scope clearly (global defaults, assistant-level overrides, thread-specific settings)
- Verify documented specifications match actual behavior and update when changes occur
- Provide clear examples and visual aids for complex configuration hierarchies

Example structure:
```json
{
  "parameters": {
    "init": {
      "model_path": "/path/to/model",
      "max_memory": "8GB"
    },
    "runtime": {
      "temperature": 0.7,
      "max_tokens": 2048
    }
  }
}
```

This prevents user confusion and ensures configurations work as documented across different scopes and contexts.