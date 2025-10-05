---
title: Enhance code clarity
description: Ensure all code examples and documentation are as clear and complete
  as possible for developers. This includes adding clarifying inline comments to explain
  non-obvious behavior, including all necessary import statements, and structuring
  information for maximum readability.
repository: TanStack/router
label: React
language: Markdown
comments_count: 6
repository_stars: 11590
---

Ensure all code examples and documentation are as clear and complete as possible for developers. This includes adding clarifying inline comments to explain non-obvious behavior, including all necessary import statements, and structuring information for maximum readability.

Key practices:
- Add inline comments to clarify behavior, especially for files or configurations that might be confusing (e.g., `// 👈🏼 ignored` for excluded files)
- Include complete import statements in code examples rather than assuming developers know what to import
- Break complex statements into separate, digestible points
- Use proper grammar and standard abbreviations (e.g., "i.e." not "ie")

Example of good clarity:
```tsx
// Include all imports
import { Link, createLink } from '@tanstack/react-router'
import { Button } from '@mui/material'

// Clear file structure with explanatory comments
routes/
├── posts.tsx
├── -posts-table.tsx // 👈🏼 ignored from route generation
├── -components/
│   ├── header.tsx // 👈🏼 ignored from route generation
│   └── footer.tsx // 👈🏼 ignored from route generation
```

This approach reduces confusion, speeds up developer onboarding, and prevents common implementation mistakes by making examples self-contained and immediately understandable.