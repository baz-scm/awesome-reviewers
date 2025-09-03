---
title: Use design system colors
description: Always use design system color variables instead of hardcoded color values
  in stylesheets. This ensures consistent theming, automatic dark/light mode support,
  and maintainable code.
repository: angular/angular
label: Code Style
language: Css
comments_count: 2
repository_stars: 98611
---

Always use design system color variables instead of hardcoded color values in stylesheets. This ensures consistent theming, automatic dark/light mode support, and maintainable code.

Replace hardcoded colors with their design system equivalents:

```scss
// ❌ Avoid hardcoded colors
.loading {
  color: #666;
  background: #f5f5f5;
}

.stat-value {
  color: #1976d2;
}

// ✅ Use design system colors
.loading {
  color: var(--secondary-contrast);
  background: var(--color-foreground);
}

.stat-value {
  color: var(--dynamic-blue-02);
}
```

Dynamic color variables (prefixed with `--dynamic-`, `--color-`, etc.) automatically adapt to theme changes, eliminating the need for manual theme-specific overrides. Only use theme mixins like `theme.dark-theme` for special cases that can't be handled by dynamic colors.