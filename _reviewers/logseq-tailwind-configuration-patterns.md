---
title: Tailwind configuration patterns
description: Follow Tailwind CSS's recommended configuration patterns to ensure proper
  functionality and JIT mode compatibility. Use the `theme.extend` object for custom
  values like font sizes, implement plugin functions for advanced customizations like
  CSS variable exposure, and explicitly safelist dynamic classes when regex patterns
  are incompatible with JIT mode.
repository: logseq/logseq
label: Configurations
language: JavaScript
comments_count: 3
repository_stars: 37695
---

Follow Tailwind CSS's recommended configuration patterns to ensure proper functionality and JIT mode compatibility. Use the `theme.extend` object for custom values like font sizes, implement plugin functions for advanced customizations like CSS variable exposure, and explicitly safelist dynamic classes when regex patterns are incompatible with JIT mode.

Example configuration structure:
```javascript
module.exports = {
  mode: 'jit',
  purge: {
    content: ['./src/**/*.js'],
    safelist: [
      "bg-red-500", "bg-blue-500", // explicit listing for JIT
    ]
  },
  plugins: [
    exposeColorsToCssVars, // custom plugin function
  ],
  theme: {
    extend: {
      fontSize: {
        '2xs': ['0.625rem', '0.875rem'] // proper extension
      },
    }
  }
}
```

This approach ensures dynamic classes aren't purged, custom functionality works correctly, and the configuration remains maintainable and compatible with Tailwind's optimization features.