---
title: Remove unnecessary elements
description: Eliminate superfluous syntax and words that don't add value to improve
  code readability and maintain consistent style. This includes removing unnecessary
  quotes in YAML files and avoiding redundant words in documentation.
repository: argoproj/argo-cd
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 20149
---

Eliminate superfluous syntax and words that don't add value to improve code readability and maintain consistent style. This includes removing unnecessary quotes in YAML files and avoiding redundant words in documentation.

For YAML files, avoid unnecessary quotes around simple string values. When quotes are required (e.g., for strings with special characters), prefer single quotes over double quotes:

```yaml
# Good
type: git
url: https://example.com
name: 'special-name-with-hyphens'

# Avoid
type: "git"
url: "https://example.com"
```

In documentation and comments, remove redundant words that don't contribute to clarity:

```markdown
# Good
Finally, after the Linter reports no errors, run git status

# Avoid
Finally, after the Linter reports no errors anymore, run git status
```

This practice reduces visual clutter, improves readability, and maintains consistent formatting standards across the codebase.