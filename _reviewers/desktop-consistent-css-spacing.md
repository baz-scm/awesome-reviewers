---
title: consistent CSS spacing
description: Ensure consistent spacing across UI components by using CSS custom properties
  for padding/margins and applying spacing only when elements exist. This prevents
  visual inconsistencies between different UI states and modes.
repository: zen-browser/desktop
label: Code Style
language: Css
comments_count: 2
repository_stars: 34711
---

Ensure consistent spacing across UI components by using CSS custom properties for padding/margins and applying spacing only when elements exist. This prevents visual inconsistencies between different UI states and modes.

Use CSS custom properties for consistent spacing values:
```css
#TabsToolbar {
  padding: var(--zen-toolbox-padding);
}
```

Apply spacing conditionally using CSS selectors to prevent unnecessary gaps:
```css
/* Only apply margin when pinned tabs exist */
#vertical-pinned-tabs-container:has(tab:not([hidden])) {
  margin-bottom: 8px;
}
```

This approach ensures that spacing remains consistent across different modes while preventing alignment issues when certain elements are not present.