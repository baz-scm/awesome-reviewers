---
title: standardize API patterns
description: Establish consistent patterns for API design, particularly for request/response
  formats and parameter structures. This improves predictability, type safety, and
  developer experience across the codebase.
repository: cypress-io/cypress
label: API
language: JavaScript
comments_count: 2
repository_stars: 48850
---

Establish consistent patterns for API design, particularly for request/response formats and parameter structures. This improves predictability, type safety, and developer experience across the codebase.

For communication interfaces, use standardized payload structures:

```js
{
  type: 'success' | 'error',
  data: any,
  event: string
}
```

For method parameters, prefer explicit options objects over method chaining when configuration is complex:

```js
// Preferred: explicit options
agent.log = (options) => {
  if (options && options.snapshot === false) {
    // handle configuration
  }
}

// Instead of: method chaining
agent.snapshot(false).log()
```

This approach makes APIs more readable, self-documenting, and easier to extend without breaking existing functionality. Consistent patterns also enable better tooling support and type checking.