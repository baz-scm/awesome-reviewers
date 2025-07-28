---
title: Consistent descriptive naming conventions
description: 'Use consistent and descriptive naming conventions across the codebase:


  1. Use kebab-case for configuration options and snake_case for internal modifiers'
repository: helix-editor/helix
label: Naming Conventions
language: Markdown
comments_count: 6
repository_stars: 39026
---

Use consistent and descriptive naming conventions across the codebase:

1. Use kebab-case for configuration options and snake_case for internal modifiers
2. Prefer descriptive names over technical terms
3. Keep names concise while maintaining clarity
4. Use semantic prefixes to group related items

Example:
```toml
# Instead of:
[editor.bufferline]
behaviour = "hidden"
matches_couter_limit = 100

# Prefer:
[editor.bufferline]
show = "never"
max-matches = 100

# Group related commands with semantic prefixes:
:align-text-left
:align-text-center
:align-text-right
```

This convention ensures consistency, improves code readability, and makes configuration more intuitive for users. Descriptive names make the purpose immediately clear, while consistent casing helps distinguish between different types of identifiers.