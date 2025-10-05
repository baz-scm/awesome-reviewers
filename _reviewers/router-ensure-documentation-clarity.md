---
title: Ensure documentation clarity
description: Documentation should be clear, accurate, and consistently structured
  to provide maximum value to developers. Avoid overly broad or inaccurate statements
  that may mislead users, and prefer explanatory content over warnings when possible.
repository: TanStack/router
label: Documentation
language: Markdown
comments_count: 4
repository_stars: 11590
---

Documentation should be clear, accurate, and consistently structured to provide maximum value to developers. Avoid overly broad or inaccurate statements that may mislead users, and prefer explanatory content over warnings when possible.

Key practices:
- Rewrite or remove unclear sections rather than leaving confusing content
- Use specific, accurate language instead of broad generalizations (e.g., "For some validation libraries..." instead of "For validation libraries...")
- Provide explanatory headings and examples instead of warnings when appropriate
- Maintain consistent formatting patterns across similar documentation sections
- Avoid duplicate headings when using frontmatter titles, as the website renders the frontmatter title as the main heading

Example of improvement:
```md
<!-- Instead of unclear or overly broad statements -->
For validation libraries we recommend using adapters...

<!-- Use more specific, accurate language -->
For some validation libraries like Zod v3, we recommend using adapters...
```

When documenting API properties, maintain consistent patterns:
```md
### `defaultOnCatch` property
- Type: `(error: Error, errorInfo: ErrorInfo) => void`
- Optional  
- Defaults to `routerOptions.defaultOnCatch`
- The default `onCatch` handler for errors caught by the Router ErrorBoundary
```

This approach ensures documentation serves as a reliable reference that developers can trust and easily understand.