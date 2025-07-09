---
title: Format for rendering compatibility
description: Documentation should be formatted appropriately for its intended rendering
  context and ensure discoverability. Consider how documentation files will be displayed
  in different environments (GitHub, websites, etc.) and choose appropriate file formats
  and structures.
repository: vercel/ai
label: Documentation
language: Markdown
comments_count: 2
repository_stars: 15590
---

Documentation should be formatted appropriately for its intended rendering context and ensure discoverability. Consider how documentation files will be displayed in different environments (GitHub, websites, etc.) and choose appropriate file formats and structures.

Key practices:
- Use `.md` instead of `.mdx` unless you specifically need MDX features and have a rendering environment that supports them
- Be mindful of how headings and formatting in files like changelogs affect rendering in different contexts
- Ensure documentation files are linked from relevant locations so users can discover them
- Move detailed guides to dedicated files in appropriate directories (like `contributing/`) to keep main documentation concise

Example:
```markdown
<!-- Good practice: Using appropriate extension and avoiding formatting that breaks rendering -->
# Contributing Guide

## Overview
Brief introduction to contribution process

## Detailed Guides
For more information, see:
- [How to create a codemod](./contributing/how-to-create-a-codemod.md)
- [Package structure](./contributing/packages.md)

## Changelog Format
When creating a changeset, avoid using headings at the beginning of the message:

```
feat(embedding-model-v2): add providerOptions
```
```

By considering the rendering context, you ensure documentation remains accessible and displays correctly across different platforms.