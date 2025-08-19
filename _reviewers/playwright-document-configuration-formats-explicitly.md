---
title: Document configuration formats explicitly
description: When documenting environment variables and configuration options, explicitly
  list all supported value formats rather than using vague descriptions. Use individual
  backticks around each supported value for clear formatting.
repository: microsoft/playwright
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 76113
---

When documenting environment variables and configuration options, explicitly list all supported value formats rather than using vague descriptions. Use individual backticks around each supported value for clear formatting.

Avoid vague descriptions like "If a number is specified, it will also be used as the terminal width." Instead, be comprehensive and specific about what formats are accepted.

Example:
```markdown
| `PLAYWRIGHT_FORCE_TTY` | | Whether to produce output suitable for a live terminal. Supports `true`, `1`, `false`, `0`, `[WIDTH]`, and `[WIDTH]x[HEIGHT]`. `[WIDTH]` and `[WIDTH]x[HEIGHT]` specifies the TTY dimensions. | `true` when terminal is in TTY mode, `false` otherwise.
```

This approach helps users understand exactly what values they can provide and reduces configuration errors by eliminating ambiguity about supported formats.