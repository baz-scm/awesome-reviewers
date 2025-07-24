---
title: Organize CSS systematically
description: 'When working with CSS/SCSS, prioritize organization and avoid duplication
  by following these principles:


  1. **Extract related styles into dedicated files** - Group thematically related
  CSS rules (like motion controls, accessibility overrides, or component variants)
  into separate SCSS files and import them centrally for better maintainability.'
repository: argoproj/argo-cd
label: Code Style
language: Css
comments_count: 2
repository_stars: 20149
---

When working with CSS/SCSS, prioritize organization and avoid duplication by following these principles:

1. **Extract related styles into dedicated files** - Group thematically related CSS rules (like motion controls, accessibility overrides, or component variants) into separate SCSS files and import them centrally for better maintainability.

2. **Leverage existing component styles** - Before writing new styles, check if similar functionality already exists in existing components. Reuse or extend existing styles rather than duplicating them.

3. **Consider all affected elements systematically** - When implementing CSS changes (especially broad ones like accessibility features), identify and address all related UI elements that should be modified consistently.

Example of good organization:
```css
// motion-control.scss - dedicated file for motion-related overrides
@media (prefers-reduced-motion: reduce) {
  .fa-spin,
  .icon.spin,
  .status-icon--spin,
  .argo-button,
  .application-resource-tree__node-animation,
  [class*="sliding-panel"],
  .argo-dropdown__content,
  .tippy-popper *,
  .Toastify--animate {
      animation: none !important;
      transition: none !important;
  }
}
```

This approach keeps styles organized, reduces code duplication, and makes the codebase more maintainable.