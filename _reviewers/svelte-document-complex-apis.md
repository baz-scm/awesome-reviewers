---
title: Document complex APIs
description: Require comprehensive JSDoc documentation for classes, complex functions,
  and all exported functions to improve codebase maintainability and developer onboarding.
  Focus especially on code with broad reach across the codebase or non-obvious functionality.
repository: sveltejs/svelte
label: Documentation
language: JavaScript
comments_count: 6
repository_stars: 83580
---

Require comprehensive JSDoc documentation for classes, complex functions, and all exported functions to improve codebase maintainability and developer onboarding. Focus especially on code with broad reach across the codebase or non-obvious functionality.

Key requirements:
- Add JSDoc to all exported functions and classes
- Document complex methods and their purpose, not just what they do
- Ensure comments are clear without assuming excessive context knowledge
- Keep documentation current when code changes

Example of good JSDoc:
```javascript
/**
 * Captures the current reactive context and returns a restore function.
 * Used to preserve effect and component state across async boundaries.
 * @param {boolean} [track=true] - Whether to track the current context
 * @returns {() => void} Function to restore the captured context
 */
export function capture(track = true) {
  // implementation
}
```

This practice makes the codebase significantly more approachable for new developers and reduces the cognitive load when working with complex APIs.