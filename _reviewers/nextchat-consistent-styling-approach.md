---
title: Consistent styling approach
description: Maintain consistency in styling approaches within components and across
  the codebase. Avoid mixing className and inline styles in the same component - choose
  one approach and stick with it throughout the component. When working with reusable
  UI library components, keep them generic by using className for styling rather than
  adding component-specific inline...
repository: ChatGPTNextWeb/NextChat
label: Code Style
language: TSX
comments_count: 2
repository_stars: 85721
---

Maintain consistency in styling approaches within components and across the codebase. Avoid mixing className and inline styles in the same component - choose one approach and stick with it throughout the component. When working with reusable UI library components, keep them generic by using className for styling rather than adding component-specific inline styles that could pollute the library's interface.

For example, instead of mixing approaches:
```tsx
// Avoid mixing styles
<div style={{ position: "relative" }}>
  <pre
    ref={ref}
    style={{
      maxHeight: collapsed ? "400px" : "none",
      overflow: "hidden",
    }}
  >
    <span className="copy-code-button">
```

Use a consistent approach with className:
```tsx
// Consistent className usage
<div className="code-container">
  <pre
    ref={ref}
    className={`code-block ${collapsed ? 'collapsed' : 'expanded'}`}
  >
    <span className="copy-code-button">
```

This improves maintainability, keeps styling logic centralized in CSS files, and maintains clean separation between UI library components and application-specific styling.