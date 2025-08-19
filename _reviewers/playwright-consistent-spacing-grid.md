---
title: consistent spacing grid
description: Use consistent spacing values that follow a standardized grid system,
  typically multiples of 4px or 8px, rather than arbitrary values. This ensures visual
  consistency across the UI and makes the design system more maintainable.
repository: microsoft/playwright
label: Code Style
language: Css
comments_count: 3
repository_stars: 76113
---

Use consistent spacing values that follow a standardized grid system, typically multiples of 4px or 8px, rather than arbitrary values. This ensures visual consistency across the UI and makes the design system more maintainable.

Avoid arbitrary spacing values like 2px, 3px, or 6px. Instead, stick to grid-based values:

```css
/* Avoid arbitrary values */
.status-passed {
  gap: 2px; /* ❌ */
}

.status-failed {
  gap: 3px; /* ❌ */
}

.container {
  gap: 6px; /* ❌ */
}

/* Use consistent grid values */
.status-passed,
.status-failed {
  gap: 4px; /* ✅ or 8px */
}

.container {
  gap: 8px; /* ✅ */
}
```

When spacing feels off visually, resist the temptation to use custom values for individual cases. Instead, evaluate whether the grid system needs adjustment or if the visual issue can be solved through other means like proper alignment or typography adjustments. This maintains design system integrity and prevents CSS from becoming inconsistent and hard to maintain.