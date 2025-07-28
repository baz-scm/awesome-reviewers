---
title: document current functionality
description: Documentation should focus exclusively on current, active functionality
  rather than including historical context, deprecated features, or legacy modes.
  Remove sections that explain how things "used to work" or provide extensive support
  for outdated approaches that have minimal user adoption.
repository: google-gemini/gemini-cli
label: Documentation
language: Markdown
comments_count: 5
repository_stars: 65062
---

Documentation should focus exclusively on current, active functionality rather than including historical context, deprecated features, or legacy modes. Remove sections that explain how things "used to work" or provide extensive support for outdated approaches that have minimal user adoption.

Avoid making unverified claims about external implementations or including speculative information. If historical context is truly necessary, move it to pull request comments or separate historical documentation rather than cluttering user-facing docs.

For example, instead of:
```markdown
> **Note:** The Memory Import Processor has evolved to support both modern compatibility with CLAUDE.md and the original GEMINI.md modular import philosophy. This dual-mode approach reflects feedback from the community...

## Import Modes: CLAUDE.md Compatibility vs. Original GEMINI.md
| Feature | CLAUDE.md Compatibility Mode (Current Default) | Original GEMINI.md Mode (Legacy) |
```

Write:
```markdown
# Memory Import Processor

The Memory Import Processor allows you to modularize your files by importing content from other markdown files using the `@file.md` syntax.
```

Similarly, replace generic template text with actual current information, and remove unnecessary elements like table of contents for short documents. Keep documentation concise and focused on what users need to know to use the current version effectively.