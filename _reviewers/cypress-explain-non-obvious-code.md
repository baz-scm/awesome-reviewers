---
title: Explain non-obvious code
description: Add explanatory comments for complex logic, workarounds, and non-obvious
  code patterns to help future maintainers understand the reasoning behind implementation
  decisions. Include links to external resources like GitHub issues, documentation,
  or source materials when relevant.
repository: cypress-io/cypress
label: Documentation
language: TypeScript
comments_count: 5
repository_stars: 48850
---

Add explanatory comments for complex logic, workarounds, and non-obvious code patterns to help future maintainers understand the reasoning behind implementation decisions. Include links to external resources like GitHub issues, documentation, or source materials when relevant.

Key areas that need explanation:
- Complex regular expressions and their expected input/output
- Workarounds and why they're necessary (with GitHub issue links)
- Unusual approaches like postMessage usage
- Complex types copied from external libraries (with source links)
- Regression fixes (with links to the issues they address)

Example:
```typescript
// Workaround for macOS focus issues - see GitHub issue #12345
resetFocusIfMacOS () {
  // Implementation here
}

// Remove file extension from filename (e.g., "Component.vue" -> "Component")
return fileName.replace(/\....?$/, '')

// Using postMessage is necessary here because we need to communicate
// across different origins in a secure context
const onPostMessage = (event) => {
  // Implementation here
}
```

This practice ensures that complex or non-obvious code decisions are documented for future developers who need to maintain, debug, or extend the functionality.