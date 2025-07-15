---
title: Defensively handle nullables
description: When working with values that could be null or undefined, implement defensive
  coding patterns to prevent runtime errors. This practice is essential for robust
  React applications.
repository: mui/material-ui
label: Null Handling
language: JavaScript
comments_count: 3
repository_stars: 96063
---

When working with values that could be null or undefined, implement defensive coding patterns to prevent runtime errors. This practice is essential for robust React applications.

Three key techniques to apply:

1. **Use double-bang (`!!`) to safely convert to boolean:**
```js
// Risky - may cause unexpected behavior if selected is undefined
props: ({ selected }) => selected,

// Safe - explicitly converts to boolean
props: ({ selected }) => !!selected,
```

2. **Apply optional chaining (`?.`) for property access and method calls:**
```js
// Risky - will throw if child or props is null/undefined
child.props.onKeyDown(event);

// Safe - gracefully handles null/undefined at any level
child?.props?.onKeyDown?.(event);
```

3. **Use ternary operators for conditional rendering:**
```js
// Risky - if productName is undefined, renders "undefined"
`${title} - ${productName}`

// Safe - handles undefined case explicitly
`${title}${productName ? ` - ${productName}` : ''}`
```

These patterns create more resilient code by anticipating and gracefully handling potential null or undefined values throughout your application.