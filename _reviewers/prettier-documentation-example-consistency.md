---
title: Documentation example consistency
description: Ensure all code examples and documentation maintain consistent formatting
  standards, use descriptive variable names, and apply proper syntax highlighting.
  This includes using meaningful identifiers instead of cryptic names like `a60`,
  applying correct language tags for syntax highlighting (e.g., `css` instead of `jsx`
  for CSS code), and providing clear...
repository: prettier/prettier
label: Code Style
language: Markdown
comments_count: 8
repository_stars: 50772
---

Ensure all code examples and documentation maintain consistent formatting standards, use descriptive variable names, and apply proper syntax highlighting. This includes using meaningful identifiers instead of cryptic names like `a60`, applying correct language tags for syntax highlighting (e.g., `css` instead of `jsx` for CSS code), and providing clear examples rather than error messages when demonstrating new features.

Examples of good practices:
- Use descriptive names: `something` instead of `a60` for imports
- Apply proper syntax highlighting: ```css for CSS code, ```ts for TypeScript
- Show working examples: `import { type A } from "mod";` instead of syntax error messages
- Maintain consistent command formats: `yarn exec prettier` across all documentation
- Use proper JSDoc formatting: `/** @type {import("prettier").Options} */`

This consistency helps developers understand features more clearly and maintains professional documentation standards across the entire codebase.