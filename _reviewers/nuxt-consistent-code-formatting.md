---
title: consistent code formatting
description: Maintain consistent formatting standards across code and documentation
  to improve readability and maintainability. This includes proper ordering of logical
  conditions and consistent use of backticks for code values in comments.
repository: nuxt/nuxt
label: React
language: TypeScript
comments_count: 2
repository_stars: 57769
---

Maintain consistent formatting standards across code and documentation to improve readability and maintainability. This includes proper ordering of logical conditions and consistent use of backticks for code values in comments.

For complex conditional statements, organize conditions in a logical order that enhances readability:

```javascript
// Better: Group related conditions and order logically
if (
  viewTransitionMode === false ||
  prefersNoTransition ||
  hasUAVisualTransition ||
  !isChangingPage(to, from)
) {
  // handle condition
}
```

In JSDoc comments and documentation, wrap code values and boolean literals in backticks for proper formatting:

```javascript
/**
 * Whether the component should render when `pending` is `true`
 * @param {boolean} showPending - Set to `true` to show loading state
 */
```

This practice ensures code is more readable for team members and maintains professional documentation standards that are especially important in React component libraries and shared codebases.