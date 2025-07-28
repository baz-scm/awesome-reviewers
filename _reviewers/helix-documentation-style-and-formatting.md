---
title: Documentation style and formatting
description: 'Maintain consistent documentation style by following these guidelines:


  1. Use concise, descriptive language for configuration and feature descriptions'
repository: helix-editor/helix
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 39026
---

Maintain consistent documentation style by following these guidelines:

1. Use concise, descriptive language for configuration and feature descriptions
2. Format keyboard commands with `<kbd>` tags: `<kbd>i</kbd>`
3. Use **bold** for mode names and important terms
4. Use hyphens (-) instead of underscores (_) in parameter names and technical terms
5. Keep descriptions clear and to-the-point

Example:
```markdown
# Configuration
| Key            | Description                  | Default |
| -------------- | ---------------------------- | ------- |
| `auto-format`  | Enable auto-formatting      | `false` |

Press <kbd>i</kbd> to enter **Insert** mode.