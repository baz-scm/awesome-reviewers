---
title: avoid hardcoded values
description: Replace hardcoded styling values and configuration constants with flexible
  alternatives to improve maintainability and consistency. Use CSS variables for colors
  and theming, backend-provided values for limits and ranges, and semantic CSS properties
  instead of absolute positioning.
repository: comfyanonymous/ComfyUI
label: Code Style
language: JavaScript
comments_count: 2
repository_stars: 83726
---

Replace hardcoded styling values and configuration constants with flexible alternatives to improve maintainability and consistency. Use CSS variables for colors and theming, backend-provided values for limits and ranges, and semantic CSS properties instead of absolute positioning.

Instead of hardcoding values:
```javascript
// Avoid this
divElement.style.backgroundColor = 'Black';
divElement.style.left = "20px";
divElement.style.position = "absolute";
max = 1920; // hardcoded limit
```

Use flexible alternatives:
```javascript
// Prefer this
divElement.style.backgroundColor = "var(--comfy-input-bg)";
divElement.style.cssFloat = "left";
divElement.style.marginRight = "4px";
max = targetWidget.options?.max; // use backend value
```

This approach makes code more maintainable by centralizing styling decisions, enables consistent theming across the application, and reduces the need to update multiple locations when requirements change. It also ensures that UI components adapt properly to different contexts and user preferences.