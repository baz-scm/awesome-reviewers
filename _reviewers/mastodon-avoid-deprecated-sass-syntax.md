---
title: avoid deprecated SASS syntax
description: Always use modern SASS and CSS syntax instead of deprecated functions
  to ensure future compatibility and avoid build warnings. Replace deprecated division
  operators with calc() or math.div(), and use native CSS functions instead of deprecated
  SASS color functions.
repository: mastodon/mastodon
label: Code Style
language: Css
comments_count: 2
repository_stars: 48691
---

Always use modern SASS and CSS syntax instead of deprecated functions to ensure future compatibility and avoid build warnings. Replace deprecated division operators with calc() or math.div(), and use native CSS functions instead of deprecated SASS color functions.

Common deprecated patterns to avoid:
- Division with `/` operator: `margin: (24px - 12px) / 2;`
- SASS color functions like `lighten()`: `fill='#{hex-color(lighten($ui-base-color, 12%))}'`

Use these modern alternatives instead:
- For division: `margin: calc((24px - 12px) / 2);` or `margin: math.div(24px - 12px, 2);`
- For color manipulation: Use CSS color mixing or native CSS color functions

This prevents deprecation warnings during builds and ensures your stylesheets remain compatible with future SASS versions. When you encounter deprecation warnings, address them immediately rather than deferring the updates.