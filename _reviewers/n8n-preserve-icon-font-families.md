---
title: Preserve icon font families
description: When working with icon elements in CSS, maintain the specialized font
  families designed for icon rendering. Replacing icon fonts (like 'element-icons')
  with standard text fonts (like 'Inter') will break icon displays that depend on
  specific glyph mappings in the icon font.
repository: n8n-io/n8n
label: Code Style
language: Css
comments_count: 2
repository_stars: 122978
---

When working with icon elements in CSS, maintain the specialized font families designed for icon rendering. Replacing icon fonts (like 'element-icons') with standard text fonts (like 'Inter') will break icon displays that depend on specific glyph mappings in the icon font.

Example of correct usage:
```css
[class^='el-icon-'],
[class*=' el-icon-'] {
  /* use !important to prevent issues with browser extensions that change fonts */
  font-family: 'element-icons' !important;
}

.selector::after {
  position: absolute;
  right: 20px;
  font-family: 'element-icons';
  content: '\e6da'; /* This glyph exists in the icon font */
}
```

Before changing font-family properties, understand their purpose in the styling system, especially when they relate to icon rendering or special visual elements.