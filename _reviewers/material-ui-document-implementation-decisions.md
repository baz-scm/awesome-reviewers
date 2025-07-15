---
title: Document implementation decisions
description: Add explanatory comments for non-obvious implementation details, especially
  when maintaining backward compatibility or implementing complex logic that isn't
  immediately clear without context. This helps other developers understand the reasoning
  behind design decisions and implementation choices.
repository: mui/material-ui
label: Documentation
language: JavaScript
comments_count: 3
repository_stars: 96063
---

Add explanatory comments for non-obvious implementation details, especially when maintaining backward compatibility or implementing complex logic that isn't immediately clear without context. This helps other developers understand the reasoning behind design decisions and implementation choices.

Example:
```javascript
const focusItem = useEventCallback((itemToFocus) => {
  if (itemToFocus === -1) {
    inputRef.current.focus();
  } else {
    // data-tag-index is kept for backward compatibility
    const indexType = renderValue ? 'data-item-index' : 'data-tag-index';
    anchorEl.querySelector(`[${indexType}="${itemToFocus}"]`).focus();
  }
});
```

This practice is especially important when:
- Maintaining backward compatibility with older APIs
- Making decisions based on usage metrics (e.g., keeping both CodeSandbox and StackBlitz)
- Creating navigation paths or references that might not be intuitive to users
- Implementing workarounds or temporary solutions

Well-documented implementation decisions reduce confusion, prevent regressions, and help new team members understand the codebase more quickly.