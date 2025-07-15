---
title: Use theme utilities consistently
description: 'Always use theme utilities for consistent styling across the application
  instead of hard-coded values. Replace direct pixel values with theme functions like
  `theme.spacing()` for spacing, and access theme variables directly with `theme.vars.*`
  for theme-aware styling:'
repository: mui/material-ui
label: Code Style
language: JavaScript
comments_count: 6
repository_stars: 96063
---

Always use theme utilities for consistent styling across the application instead of hard-coded values. Replace direct pixel values with theme functions like `theme.spacing()` for spacing, and access theme variables directly with `theme.vars.*` for theme-aware styling:

```js
// Don't
padding: 16,
paddingBottom: 24,

// Do
padding: theme.spacing(2),
paddingBottom: theme.spacing(3),
```

For complex component styling, prefer the `styled` API over the `sx` prop as it offers better performance and readability, especially with longer style definitions:

```js
// Less optimal for complex styling
<ToggleButtonGroup
  sx={(theme) => ({
    gap,
    ...(orientation === 'horizontal' && {
      // many complex styles...
    })
  })}
/>

// Better for complex styling
const StyledToggleButtonGroup = styled(ToggleButtonGroup)(({ theme }) => ({
  gap: props.gap,
  ...(props.orientation === 'horizontal' && {
    // many complex styles...
  })
}));
```

Choose the simplest CSS solutions possible and avoid unnecessary inline comments for self-explanatory style changes. When modifying properties, use specific CSS properties (like `overflowY: 'auto'` instead of `overflow: 'auto'`) when the intent is clear.