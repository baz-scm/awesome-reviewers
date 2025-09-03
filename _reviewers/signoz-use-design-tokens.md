---
title: use design tokens
description: Replace hardcoded color values, spacing, and other design-related constants
  with design tokens or CSS custom properties. This promotes consistency across the
  application, makes theme changes easier to implement, and reduces code duplication.
repository: SigNoz/signoz
label: Code Style
language: Css
comments_count: 3
repository_stars: 23369
---

Replace hardcoded color values, spacing, and other design-related constants with design tokens or CSS custom properties. This promotes consistency across the application, makes theme changes easier to implement, and reduces code duplication.

For colors, use predefined design system tokens:
```scss
// Instead of:
border-right: 1px solid #1d212d;
color: var(--text-color-secondary);

// Use:
border-right: 1px solid var(--bg-slate-400);
background: var(--bg-slate-500);
```

For repeated values that don't have existing tokens, declare local CSS variables to avoid repetition and improve maintainability. This ensures a consistent visual language and makes global design changes more manageable.