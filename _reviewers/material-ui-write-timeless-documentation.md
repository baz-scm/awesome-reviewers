---
title: Write timeless documentation
description: Documentation should be written to remain clear and useful regardless
  of when it's read. Avoid references to temporary contexts like "in this PR," "original
  behavior," or "current implementation" that will lose meaning over time. Instead,
  precisely describe behaviors, changes, and functionality in a way that will remain
  clear to developers reading the code...
repository: mui/material-ui
label: Documentation
language: TypeScript
comments_count: 2
repository_stars: 96063
---

Documentation should be written to remain clear and useful regardless of when it's read. Avoid references to temporary contexts like "in this PR," "original behavior," or "current implementation" that will lose meaning over time. Instead, precisely describe behaviors, changes, and functionality in a way that will remain clear to developers reading the code months or years later. This applies to API documentation, inline code comments, and technical documentation.

Example:
```javascript
// Instead of:
// If no layer is specified, use the original behavior

// Write:
// If no layer is specified, add style and clean it on unmount
```

When documenting breaking changes, be explicit about what needs to be updated and why the change was made, rather than relying on contextual knowledge that may be forgotten.