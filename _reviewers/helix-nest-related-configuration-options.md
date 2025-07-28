---
title: Nest related configuration options
description: Group related configuration options into nested TOML sections rather
  than using flat key-value pairs. This improves readability, maintainability, and
  makes relationships between settings more explicit.
repository: helix-editor/helix
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 39026
---

Group related configuration options into nested TOML sections rather than using flat key-value pairs. This improves readability, maintainability, and makes relationships between settings more explicit.

Example:
Instead of:
```toml
word-completion = true
word-completion-trigger-length = 7
```

Use:
```toml
[word-completion]
enable = true
trigger-length = 7
```

This approach:
- Makes configuration hierarchies clear
- Groups related settings together
- Reduces naming conflicts and redundancy
- Improves configuration file organization
- Makes it easier to add related options in the future

When adding new configuration options, consider if they logically belong in an existing section or warrant creating a new nested section.