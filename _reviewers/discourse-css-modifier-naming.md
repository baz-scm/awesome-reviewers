---
title: CSS modifier naming
description: Use consistent modifier patterns with `--` prefixes for CSS classes and
  variables. Prefer semantic base names combined with modifiers over long descriptive
  names. This approach improves maintainability and creates predictable naming schemes.
repository: discourse/discourse
label: Naming Conventions
language: Css
comments_count: 3
repository_stars: 44898
---

Use consistent modifier patterns with `--` prefixes for CSS classes and variables. Prefer semantic base names combined with modifiers over long descriptive names. This approach improves maintainability and creates predictable naming schemes.

For CSS classes, use BEM-like modifier syntax:
```scss
.filter-tip__button {
  &.--selected {  // Use -- prefix for modifiers
    background: var(--primary);
  }
}
```

For CSS variables, group related properties using modifier patterns:
```scss
:root {
  --title-color: var(--primary);
  --title-color--header: var(--header_primary);  // Related modifier
}
```

For component names, use concise base names with modifiers rather than long descriptive names:
```scss
// Prefer this:
.empty-state {
  &.--topic-filter { }
}

// Over this:
.empty-topic-filter-education { }
```