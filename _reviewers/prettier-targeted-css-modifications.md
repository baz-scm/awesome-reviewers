---
title: targeted CSS modifications
description: Make targeted, purposeful CSS modifications that either enhance visual
  presentation or fix specific functionality issues without disrupting existing styles.
  When adding new styles, focus on specific improvements like centering text or adjusting
  colors. When modifying existing styles, preserve the original intent and make minimal
  changes to address the...
repository: prettier/prettier
label: Code Style
language: Css
comments_count: 2
repository_stars: 50772
---

Make targeted, purposeful CSS modifications that either enhance visual presentation or fix specific functionality issues without disrupting existing styles. When adding new styles, focus on specific improvements like centering text or adjusting colors. When modifying existing styles, preserve the original intent and make minimal changes to address the specific problem.

For example, instead of changing existing padding values, adjust positioning properties to fix overlapping issues:

```css
/* Good: Targeted addition for visual improvement */
.sponsorsSection h2 {
  text-align: center;
}

/* Good: Minimal adjustment to fix functionality */
.button {
  top: -5px; 
  right: 16px;
}
```

This approach maintains code stability while allowing for necessary improvements and fixes.