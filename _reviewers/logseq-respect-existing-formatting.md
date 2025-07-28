---
title: Respect existing formatting
description: When modifying existing files, maintain the formatting and style conventions
  already established in those files rather than imposing new formatting standards.
  This includes respecting existing whitespace patterns, indentation styles, and structural
  formatting choices.
repository: logseq/logseq
label: Code Style
language: Markdown
comments_count: 2
repository_stars: 37695
---

When modifying existing files, maintain the formatting and style conventions already established in those files rather than imposing new formatting standards. This includes respecting existing whitespace patterns, indentation styles, and structural formatting choices.

For documentation files, ensure consistency with existing patterns such as proper spacing between headers and content. For code files, follow the existing whitespace and indentation conventions of the file being modified.

Example:
```markdown
## Auto-formatting

[cljfmt](https://cljdoc.org/d/cljfmt/cljfmt/0.9.0/doc/readme) is a common formatter...
```

The principle is that contributions should harmonize with the existing codebase style rather than introduce formatting inconsistencies, even if the new formatting might be considered "better" in isolation.