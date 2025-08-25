---
title: prefer CSS custom properties
description: Use CSS custom properties (CSS variables) instead of hardcoded values
  for fonts, spacing, colors, and other design tokens. This improves maintainability,
  enables consistent theming, and makes design system changes easier to implement
  across the codebase.
repository: discourse/discourse
label: Code Style
language: Css
comments_count: 3
repository_stars: 44898
---

Use CSS custom properties (CSS variables) instead of hardcoded values for fonts, spacing, colors, and other design tokens. This improves maintainability, enables consistent theming, and makes design system changes easier to implement across the codebase.

Examples of preferred patterns:
```css
/* Good - uses custom properties */
font-family: var(--font-family);
margin-bottom: var(--space-2);
border: 1px solid var(--content-border-color);

/* Avoid - hardcoded values */
font-family: system-ui, Arial, sans-serif;
margin-bottom: 10px;
border: 1px solid var(--primary-low);
```

When choosing custom properties, use semantic names that reflect the property's purpose (like `--content-border-color` for content separation vs `--input-border-color` for form inputs) rather than generic color names.