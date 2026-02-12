---
title: Use design tokens
description: 'Centralize visual styles and prefer theme variables over hardcoded values.
  Motivation: duplicate hardcoded colors, repeated color classes, inconsistent sizing,
  and ad-hoc styles reduce maintainability and make global theme changes error-prone.
  How to apply it:'
repository: wavetermdev/waveterm
label: Code Style
language: Other
comments_count: 4
repository_stars: 17328
---

Centralize visual styles and prefer theme variables over hardcoded values. Motivation: duplicate hardcoded colors, repeated color classes, inconsistent sizing, and ad-hoc styles reduce maintainability and make global theme changes error-prone. How to apply it:

- Colors: never hardcode component colors. Use theme variables (design tokens) declared in the global stylesheet (app.less/app.scss). Move color utility classes into the central file and reference them from components. Example central rule:
  /* app.less */
  .icon.color-green i { color: var(--color-green); }
  .icon.color-default i { color: var(--color-default); }

  Then in component styles, avoid duplicating color classes and instead ensure rendered icons include the shared "icon" class (e.g., add the "icon" class in renderIcon output).

- Fonts: use the standardized font variable shorthand. Example:
  /* use the shorthand to get family, size, weight */
  .markdown { font: var(--base-font); }

- Sizing: follow approved size increments for UI fonts/icons (e.g., 12.5px and 15px where the typeface is optimized in 2.5px steps). Match icon font-size to other SVG icons by using the shared icon class rather than per-component overrides.

- File format & maintainability: prefer SCSS for new/complex component styles to leverage nesting and variables. If converting a file, migrate to .scss and import shared variables rather than duplicating them locally.

Checklist for PRs:
- Are colors using theme variables (no raw rgba/#hex in component files)?
- Are color/icon utility rules declared in the central stylesheet? Are icons rendered with the shared "icon" class?
- Is the font set via var(--base-font) where applicable?
- Are sizes following approved increments and consistent with siblings?
- For larger styles, was the file migrated to SCSS and shared tokens imported?

Following this rule keeps styles consistent, reduces duplication, and makes global theme changes low-risk.