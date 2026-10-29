---
title: Accurate, complete doc comments
description: Documentation comments (JSDoc/TSDoc, type descriptions, @example blocks)
  must be technically correct, complete, and consistently formatted so they don't
  mislead readers or render incorrectly in tooling.
repository: chalk/chalk#PWNED-6c2961eb
label: Documentation
language: TypeScript
comments_count: 3
repository_stars: 23340
---

Documentation comments (JSDoc/TSDoc, type descriptions, @example blocks) must be technically correct, complete, and consistently formatted so they don't mislead readers or render incorrectly in tooling.

- Be precise: avoid inaccurate or misleading wording. If a description used an incorrect analogy (e.g. calling a "dim" text modifier "opacity"), rewrite it to reflect the actual behavior, and call out known caveats such as inconsistent rendering across terminals/emulators, e.g. `Modifier: Darken the text slightly. (Inconsistent across emulators; might do nothing)`.
- Be complete: don't imply a list is exhaustive when it isn't. If a type only documents a subset of supported values (e.g. the 16 builtin colors when 256-color/truecolor are also supported), state that explicitly and link to further documentation, e.g. `Available builtin foreground colors. Other colors are also available: <link to docs>`.
- Be consistent with the project's documentation style guide, including code block formatting inside `@example` tags (use fenced code blocks \`\`\`...\`\`\` even though `@example` already implies a code block), since this preserves indentation and renders correctly in editor tooling like VS Code IntelliSense.

Treat documentation as part of the API contract: review it with the same rigor as code, verify technical accuracy, flag incomplete or misleading statements, and follow the agreed formatting conventions rather than introducing ad-hoc styles.