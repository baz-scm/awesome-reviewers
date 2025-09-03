---
title: Markdown formatting consistency
description: Ensure consistent markdown formatting in documentation by wrapping all
  technical terms, API names, property names, and code-related content in backticks.
  This improves readability and maintains visual consistency across documentation.
repository: ant-design/ant-design
label: Code Style
language: Markdown
comments_count: 6
repository_stars: 95882
---

Ensure consistent markdown formatting in documentation by wrapping all technical terms, API names, property names, and code-related content in backticks. This improves readability and maintains visual consistency across documentation.

**Examples of proper formatting:**
- Property names: `classNames`, `styles`, `href`, `variant`
- API attributes: `aria-*`, `shape="round"`
- Technical terms: `@layer antd`

**Common mistakes to avoid:**
- Writing `classNames` instead of `classNames`
- Using plain text for property values like `variant="filled"` instead of `variant="filled"`
- Missing backticks around technical terms in changelog entries

This standard ensures that code-related content is visually distinguished from regular text, making documentation easier to scan and understand for developers.