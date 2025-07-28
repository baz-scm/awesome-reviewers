---
title: Document error handling limitations
description: When documenting error handling mechanisms, always provide complete context
  about how they work, including any limitations, edge cases, and alternative approaches.
  This prevents developers from making incorrect assumptions about behavior.
repository: electron/electron
label: Error Handling
language: Markdown
comments_count: 3
repository_stars: 117644
---

When documenting error handling mechanisms, always provide complete context about how they work, including any limitations, edge cases, and alternative approaches. This prevents developers from making incorrect assumptions about behavior.

For example, when documenting warning suppression flags, clarify that suppression only affects default handlers while programmatic handling remains available:

```js
// Even with --no-warnings, apps can still handle warnings
process.on('warning', (warning) => {
  // Custom warning handling logic
});
```

Similarly, when documenting error handling behavior changes, ensure code examples accurately reflect the actual behavior and mention any known limitations:

```js
// Note: process.exit() may not synchronously crash utility processes
process.on('unhandledRejection', () => {
  process.exit(1); // May have timing issues in utility processes
});
```

This approach helps developers understand the full scope of error handling mechanisms and make informed implementation decisions.