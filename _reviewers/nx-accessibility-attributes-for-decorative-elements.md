---
title: accessibility attributes for decorative elements
description: Decorative images, icons, and other visual elements that don't convey
  meaningful content should include `aria-hidden="true"` to prevent screen readers
  from announcing them. This ensures a cleaner experience for users with assistive
  technologies and maintains consistent accessibility markup patterns across the codebase.
repository: nrwl/nx
label: Code Style
language: Other
comments_count: 2
repository_stars: 27518
---

Decorative images, icons, and other visual elements that don't convey meaningful content should include `aria-hidden="true"` to prevent screen readers from announcing them. This ensures a cleaner experience for users with assistive technologies and maintains consistent accessibility markup patterns across the codebase.

Apply this attribute to any img, svg, or icon elements that serve purely decorative purposes:

```html
<!-- Decorative sidebar icon -->
<img 
  src={icon} 
  alt="" 
  aria-hidden="true" 
  class="sidebar-icon w-4 h-4 dark:invert"
/>

<!-- Decorative group icon -->
<img 
  src={icon} 
  alt="" 
  aria-hidden="true" 
  class="sidebar-icon w-4 h-4 dark:invert"
/>
```

This practice should be consistently applied to maintain clean, accessible markup throughout the application.