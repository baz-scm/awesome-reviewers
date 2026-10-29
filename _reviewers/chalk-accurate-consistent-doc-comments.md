---
title: Accurate, consistent doc comments
description: Doc comments and type definitions must precisely describe the full behavior
  of the API, not just a subset. If a type or function supports more options than
  are explicitly listed (e.g., additional colors beyond the named enum values), state
  this clearly and link to the canonical reference for the complete details, rather
  than letting the comment imply an...
repository: chalk/chalk
label: Documentation
language: TypeScript
comments_count: 3
repository_stars: 23342
---

Doc comments and type definitions must precisely describe the full behavior of the API, not just a subset. If a type or function supports more options than are explicitly listed (e.g., additional colors beyond the named enum values), state this clearly and link to the canonical reference for the complete details, rather than letting the comment imply an exhaustive list. For example, instead of "Available foreground colors", prefer "Available builtin foreground colors. Other colors are also available: <link>".

Code examples embedded in doc comments (e.g., `@example` blocks) must follow the team's established style guide for formatting — use fenced code blocks (triple backticks) consistently, even though `@example` already implies a code block, since this preserves indentation and renders correctly in IDE tooltips (e.g., VS Code IntelliSense). Don't deviate from the style guide without first proposing and agreeing on an amendment to it.

When documenting types or wrappers around external packages, consider whether referencing or re-exporting canonical source definitions (instead of duplicating documentation/types) would better keep docs accurate and in sync with the underlying implementation.</description>
</invoke>
