---
title: consistent formatting choices
description: Maintain consistent formatting and structural choices throughout the
  codebase to improve readability and maintainability. This includes always using
  braces for control structures (even single-line statements), choosing appropriate
  control flow constructs for clarity, and organizing code to prevent execution order
  issues.
repository: facebook/yoga
label: Code Style
language: JavaScript
comments_count: 3
repository_stars: 18255
---

Maintain consistent formatting and structural choices throughout the codebase to improve readability and maintainability. This includes always using braces for control structures (even single-line statements), choosing appropriate control flow constructs for clarity, and organizing code to prevent execution order issues.

Key practices:
- Always use braces for if statements, loops, and other control structures, even for single lines
- Choose simpler control structures (if/else over switch) when they improve readability
- Place critical code early in functions to avoid accidental skipping due to early returns

Example of consistent brace usage:
```javascript
// Good - always use braces
if (!node.lastLayout) {
  node.lastLayout = {};
}

// Avoid - inconsistent formatting
if (!node.lastLayout) node.lastLayout = {};
```

Example of clearer control structure:
```javascript
// Preferred for simple cases
if (typeof val === 'number') {
  obj[key] = roundNumber(val);
} else if (typeof val === 'object') {
  inplaceRoundNumbersInObject(val);
}

// Instead of switch for simple type checking
```

These consistent choices make code more predictable for team members and reduce cognitive load during code reviews.