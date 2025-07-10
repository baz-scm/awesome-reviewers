---
title: Document compatibility boundaries
description: 'Clearly communicate your API''s compatibility guarantees and limitations.
  When designing APIs, explicitly indicate what usage patterns are supported vs. which
  are experimental or might change. For functions that have multiple calling patterns,
  document which are stable and which might be deprecated:'
repository: mui/material-ui
label: API
language: Markdown
comments_count: 4
repository_stars: 96063
---

Clearly communicate your API's compatibility guarantees and limitations. When designing APIs, explicitly indicate what usage patterns are supported vs. which are experimental or might change. For functions that have multiple calling patterns, document which are stable and which might be deprecated:

```javascript
// GOOD: Clear documentation about compatibility
/**
 * Creates a theme based on the options received.
 * @param {object} options - The theme options to use
 * @returns {object} A complete theme object
 * @note Only the first argument is processed by this function.
 * While passing multiple arguments currently works for backward 
 * compatibility, this behavior may be removed in future versions.
 * To ensure forward-compatibility, manually deep merge theme objects
 * and pass the result as a single object.
 */
function createTheme(options, ...args) {
  // implementation
}
```

When documenting API changes or limitations, use precise language that accurately reflects their status:

1. For deprecated features, provide explicit migration paths
2. For versioning decisions, clearly explain the technical reasoning
3. For import patterns and access restrictions, document what's considered public API vs. internal implementation

This transparency helps users make informed decisions about adoption, upgrades, and implementation strategies while reducing confusion about API boundaries.