---
title: Consistent Markdown Formatting
description: 'Make Markdown generation deterministic and parser-safe.


  1) Quote frontmatter/template variables

  - When using placeholders like `{{description}}` in Markdown frontmatter, wrap the
  value in quotes to prevent Antigravity/CLI parsing from breaking on special character
  sequences (e.g., ` #`, `: `).'
repository: bmad-code-org/bmad-method
label: Code Style
language: Markdown
comments_count: 3
repository_stars: 51859
---

Make Markdown generation deterministic and parser-safe.

1) Quote frontmatter/template variables
- When using placeholders like `{{description}}` in Markdown frontmatter, wrap the value in quotes to prevent Antigravity/CLI parsing from breaking on special character sequences (e.g., ` #`, `: `).

Example:
```md
---
description: "{{description}}"
---
```

2) Enforce the same Markdown lint/format rules
- Ensure everyone uses the same markdownlint/formatter plugin configuration.
- Follow the agreed code-fence convention (e.g., nesting uses more ticks; avoid unnecessary fence-depth changes).
- Gate formatting by running the formatter/linter via pre-commit or a pre-push hook (e.g., Husky) so running `validate` doesn’t produce large, unexpected diffs.

Result: fewer parser-loading issues in templates and smaller, consistent diffs from formatting tooling.