---
title: Use design system tokens
description: Always use design system tokens (theme values, breakpoints, spacing units)
  instead of hard-coded values. This ensures consistency across the codebase and makes
  maintenance easier when design changes are needed.
repository: mui/material-ui
label: Code Style
language: TSX
comments_count: 3
repository_stars: 96063
---

Always use design system tokens (theme values, breakpoints, spacing units) instead of hard-coded values. This ensures consistency across the codebase and makes maintenance easier when design changes are needed.

Bad:
```tsx
{% raw %}
<Grid sx={{ 
  width: '44px',
  fontWeight: 'bold',
  '@media (max-width: 640px)': {
    // ...
  }
}} />
{% endraw %}
```

Good:
```tsx
{% raw %}
<Grid sx={{ 
  width: theme.spacing(5.5), // or appropriate token
  fontWeight: theme.typography.fontWeightBold,
  [theme.breakpoints.down('sm')]: {
    // ...
  }
}} />
{% endraw %}
```

This practice:
- Maintains visual consistency
- Simplifies theme customization
- Makes responsive design more maintainable
- Reduces the need for magic numbers in the code