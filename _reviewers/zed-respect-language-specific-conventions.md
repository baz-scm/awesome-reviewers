---
title: Respect language-specific conventions
description: 'Always adhere to the established formatting and syntax conventions of
  each programming language while maintaining consistency across related language
  configurations. This includes:'
repository: zed-industries/zed
label: Code Style
language: Toml
comments_count: 3
repository_stars: 62119
---

Always adhere to the established formatting and syntax conventions of each programming language while maintaining consistency across related language configurations. This includes:

1. Using the correct indentation style for each language (e.g., hard tabs for Go)
2. Applying similar configurations to related languages (e.g., if adding block comments to JavaScript, also add them to TypeScript)
3. Maintaining consistent organization within configuration files (e.g., keeping dependencies sorted alphabetically)

Example:
```toml
# For Go
tab_size = 4
hard_tabs = true

# For JavaScript and related languages
line_comments = ["// "]
block_comment = ["/*", "*/"]
```

Following language-specific conventions improves code readability, leverages standard tooling, and helps maintain consistency across the codebase, especially when working with multiple languages in the same project.