---
title: Use supported documentation formats
description: 'When updating documentation, examples, or config-related code:


  1) Follow the source of truth for generated artifacts

  - **Do** change the upstream schema/config file.'
repository: mermaid-js/mermaid
label: Documentation
language: TypeScript
comments_count: 6
repository_stars: 87952
---

When updating documentation, examples, or config-related code:

1) Follow the source of truth for generated artifacts
- **Do** change the upstream schema/config file.
- **Don’t** edit generated files directly.

2) Use the supported frontmatter format for diagram configuration
- **Do** use frontmatter (e.g., `---` block) to set config/theme.
- **Don’t** rely on deprecated directive init syntax like `%%{init: ...}%%` in tests/examples.

Example (frontmatter-style):
```md
---
title: Timeline example
theme: forest
config:
  logLevel: debug
---

timeline
  title Timeline Title
```

3) Prefer storing diagram sources in `.mmd` (or Markdown) for better developer ergonomics
- Keep an `index.ts` for metadata, and put each diagram in a corresponding `*.mmd` file for IDE syntax highlighting/plugins.

4) Avoid brittle Markdown “massaging”
- If you need indentation normalization, use a safe helper like `dedent()` instead of regex-based whitespace stripping (to prevent breaking lists and indented code blocks).